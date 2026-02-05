# RAG with Google File Search

A simple and powerful web application built with Streamlit that allows users to upload PDF files and ask questions using Google's File Search RAG (Retrieval Augmented Generation) system.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![Google AI](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)

## 🌟 Features

- 📤 **Drag and Drop Upload** - Easy PDF file upload interface
- 🤖 **Google File Search RAG** - Fully automated RAG system using Google's File Search
- 💬 **Interactive Chat** - Natural language Q&A interface
- 🔍 **Source Citations** - See which documents were used to answer your questions
- 🎯 **Multiple Models** - Choose from various Gemini models
- 🔒 **Secure** - API key stored only in browser session
- 📚 **Multi-Document Support** - Upload and query multiple PDFs simultaneously
- ⚡ **Smart Error Handling** - Helpful guidance for quota limits and errors

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rag_website.git
   cd rag_website
   ```

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

## 📖 Usage

1. **Enter API Key**: Paste your Gemini API key in the sidebar
2. **Select Model**: Choose a Gemini model from the dropdown
3. **Upload PDFs**: Drag and drop your PDF files
4. **Ask Questions**: Type questions in the chat interface
5. **View Sources**: Expand the "Sources" section to see which documents were cited

## 🛠️ How It Works

The application uses Google's File Search API to implement RAG:

1. **Upload**: PDFs are uploaded to a Google File Search Store
2. **Index**: Google automatically indexes the document content
3. **Query**: When you ask a question, File Search retrieves relevant passages
4. **Generate**: Gemini generates accurate answers based on the retrieved context
5. **Cite**: The app shows which documents were used as sources

## 📦 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Python web framework
- **AI Backend**: [Google Gemini](https://ai.google.dev/) - Advanced AI models
- **RAG System**: [Google File Search](https://ai.google.dev/gemini-api/docs/file-search) - Automated retrieval system

## 🔑 Environment Variables

No environment variables required - API key is entered through the UI for security.

## ⚠️ Error Handling

The app includes intelligent error handling:

- **Quota Exceeded**: Provides guidance to switch models or upgrade API plan
- **File Processing**: Clear feedback on upload and processing status
- **Source Mapping**: Displays original filenames instead of system-generated names

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for the Gemini API and File Search functionality
- Streamlit for the excellent web framework
- The open-source community

## 📧 Contact

Project Link: [https://github.com/YOUR_USERNAME/rag_website](https://github.com/YOUR_USERNAME/rag_website)

---

Made with ❤️ using Streamlit and Google Gemini
