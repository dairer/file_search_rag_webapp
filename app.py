import streamlit as st
from google import genai
from google.genai import types
import tempfile
import time
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="RAG with Google File Search",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("RAG with Google File Search")
st.markdown(
    "Upload PDF files and ask questions about their content using Google File Search."
)

# Session state initialization
session_defaults = {
    "api_key": None,
    "client": None,
    "uploaded_files": [],
    "file_search_store": None,
    "chat_history": [],
    "file_name_mapping": {},  # Maps Gemini file IDs/titles to original filenames
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Sidebar: configuration
with st.sidebar:
    st.header("Configuration")

    api_key_input = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        help="Get your API key from https://aistudio.google.com/app/apikey",
    )

    st.caption(
        "🔐 Your API key is used only for this session and is never stored. "
        "Use a restricted or test key when possible."
    )

    # Initialize client only if key changes
    if api_key_input:
        if st.session_state.api_key != api_key_input:
            try:
                st.session_state.api_key = api_key_input
                st.session_state.client = genai.Client(api_key=api_key_input)

                # Reset dependent state
                st.session_state.file_search_store = None
                st.session_state.uploaded_files = []
                st.session_state.chat_history = []

            except Exception as e:
                st.error(f"Failed to initialize client: {e}")
                st.stop()

    # Model selection
    selected_model = None
    if st.session_state.client:
        available_models = [
            "gemini-3-pro-preview",
            "gemini-3-flash-preview",
            "gemini-2.5-pro",
            "gemini-2.5-flash-lite",
        ]

        selected_model = st.selectbox(
            "Select Model",
            options=available_models,
            help="Choose a Gemini model for File Search–augmented generation",
        )

    st.markdown("---")

# Guard rails (make sure api is provided)
if not st.session_state.client:
    st.warning("Please enter a valid Gemini API key to continue.")
    st.stop()

if not selected_model:
    st.warning("Please select a model.")
    st.stop()

# File upload
st.header("Upload PDF Files")

uploaded_files = st.file_uploader(
    "Drag and drop PDF files here",
    type=["pdf"],
    accept_multiple_files=True,
)

# Process uploads (create google file store
if uploaded_files and uploaded_files != st.session_state.uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.session_state.file_search_store = None
    st.session_state.chat_history = []
    st.session_state.file_name_mapping = {}  # Reset mapping

    with st.spinner("Creating File Search Store and uploading PDFs..."):
        try:
            client = st.session_state.client

            store = client.file_search_stores.create()
            #st.success(f"Created File Search Store: `{store.name}`")
            st.success(f"Created File Search Store")


            for uploaded_file in uploaded_files:
                st.info(f"Uploading `{uploaded_file.name}`")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                upload_op = client.file_search_stores.upload_to_file_search_store(
                    file_search_store_name=store.name,
                    file=tmp_path,
                )

                while not upload_op.done:
                    time.sleep(2)
                    upload_op = client.operations.get(upload_op)

                # Store the mapping between uploaded file and original name
                # The title in grounding context will be the temp file path or similar
                # We'll map based on the file we just uploaded
                if hasattr(upload_op, 'result') and upload_op.result:
                    result = upload_op.result
                    # Map the result file name/id to original filename
                    if hasattr(result, 'name'):
                        st.session_state.file_name_mapping[result.name] = uploaded_file.name
                    if hasattr(result, 'display_name'):
                        st.session_state.file_name_mapping[result.display_name] = uploaded_file.name
                
                # Also map the temp path to original name (as fallback)
                st.session_state.file_name_mapping[Path(tmp_path).name] = uploaded_file.name
                st.session_state.file_name_mapping[tmp_path] = uploaded_file.name

                Path(tmp_path).unlink(missing_ok=True)
                st.success(f"Uploaded `{uploaded_file.name}`")

            st.session_state.file_search_store = store
            st.success("All files processed successfully.")

        except Exception as e:
            st.error(f"File processing failed: {e}")
            st.stop()

# Show uploaded files
if st.session_state.uploaded_files:
    with st.expander("Uploaded Files"):
        for i, f in enumerate(st.session_state.uploaded_files, 1):
            st.write(f"{i}. {f.name} ({f.size / 1024:.1f} KB)")

        if st.session_state.file_search_store:
            st.write(f"**Store:** `{st.session_state.file_search_store.name}`")

# Chat interface
if st.session_state.file_search_store:
    st.header("Chat with your documents")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating response..."):
                try:
                    response = st.session_state.client.models.generate_content(
                        model=selected_model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            tools=[
                                types.Tool(
                                    file_search=types.FileSearch(
                                        file_search_store_names=[
                                            st.session_state.file_search_store.name
                                        ]
                                    )
                                )
                            ]
                        ),
                    )

                    answer = response.text or "_No response generated._"
                    st.markdown(answer)

                    # Grounding sources
                    if response.candidates:
                        grounding = response.candidates[0].grounding_metadata
                        if grounding and grounding.grounding_chunks:
                            with st.expander("Sources"):
                                sources = set()
                                for c in grounding.grounding_chunks:
                                    if c.retrieved_context:
                                        title = c.retrieved_context.title
                                        
                                        # Try to map to original filename
                                        original_name = None
                                        
                                        # Check if title matches any mapping key
                                        if title in st.session_state.file_name_mapping:
                                            original_name = st.session_state.file_name_mapping[title]
                                        else:
                                            # Try to find a partial match (e.g., title contains temp path)
                                            for key, value in st.session_state.file_name_mapping.items():
                                                if key in title or title in key:
                                                    original_name = value
                                                    break
                                        
                                        # If we couldn't map it, try to match against uploaded file names
                                        if not original_name:
                                            for uploaded_file in st.session_state.uploaded_files:
                                                # Check if the uploaded filename appears in the title
                                                if uploaded_file.name in title:
                                                    original_name = uploaded_file.name
                                                    break
                                        
                                        # Use original name if found, otherwise use the title from Gemini
                                        display_name = original_name if original_name else title
                                        sources.add(display_name)
                                
                                if sources:
                                    for src in sorted(sources):
                                        st.write(f"- {src}")
                                else:
                                    st.write("No specific sources cited.")

                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )

                except Exception as e:
                    error_str = str(e).lower()
                    
                    # Check for quota/rate limit errors
                    if any(keyword in error_str for keyword in [
                        "quota", "rate limit", "429", "resource exhausted", 
                        "too many requests", "quota exceeded", "insufficient quota"
                    ]):
                        error_msg = "⚠️ **API Quota Exceeded**\n\n"
                        error_msg += "You've reached your API usage limit. Please try one of the following:\n\n"
                        error_msg += "1. **Switch to a different model** - Try selecting a different model from the sidebar (e.g., switch from Pro to Flash)\n"
                        error_msg += "2. **Wait and retry** - Rate limits reset after a period of time\n"
                        error_msg += "3. **Upgrade your API plan** - Visit [Google AI Studio](https://aistudio.google.com/) to upgrade your subscription\n"
                        error_msg += "4. **Use a different API key** - If you have another API key with available quota\n\n"
                        error_msg += f"_Original error: {e}_"
                        st.error(error_msg)
                    else:
                        error_msg = f"Error generating response: {e}"
                        st.error(error_msg)
                    
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": f"Error: {e}"}
                    )

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

else:
    st.info("Upload one or more PDF files to begin.")

st.markdown("---")
