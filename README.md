# RAG with Google File Search

A Streamlit-based web application that lets users upload PDF files and ask questions using Google’s File Search–based Retrieval Augmented Generation (RAG) workflow.

The web app is available online [here](https://simple-research-rag.streamlit.app/)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![Google AI](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)

## Features

- PDF upload via drag and drop
- Retrieval Augmented Generation using Google File Search
- Chat-style interface for natural language questions
- Source citations showing which documents informed each answer
- Support for multiple Gemini models
- API key stored only in the browser session
- Ability to upload and query multiple PDFs at once
- Clear error handling for quota limits and API issues

## Getting Started

### Prerequisites

- Python 3.8 or higher  
- Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rag_website.git
   cd rag_website

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** at `http://localhost:8501`

## Usage

1. **Enter API Key**: Paste your Gemini API key in the sidebar
2. **Select Model**: Choose a Gemini model from the dropdown
3. **Upload PDFs**: Drag and drop your PDF files
4. **Ask Questions**: Type questions in the chat interface
5. **View Sources**: Expand the "Sources" section to see which documents were cited

## How It Works

The application uses Google's File Search API to implement RAG:

1. **Upload**: PDFs are uploaded to a Google File Search Store
2. **Index**: Google automatically indexes the document content
3. **Query**: When you ask a question, File Search retrieves relevant passages
4. **Generate**: Gemini generates accurate answers based on the retrieved context
5. **Cite**: The app shows which documents were used as sources

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Python web framework
- **AI Backend**: [Google Gemini](https://ai.google.dev/)
- **RAG System**: [Google File Search](https://ai.google.dev/gemini-api/docs/file-search) - Automated retrieval system

## Environment Variables

No environment variables required - API key is entered through the UI for security.
