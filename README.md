# Smart Document Q&A Pipeline

A simple, end-to-end document understanding pipeline designed to demonstrate Large Language Model (LLM) integration using a modern tech stack. Built with **React** on the frontend and **FastAPI** on the backend, this project supports document upload, semantic search, and LLM-based question answering.

This project supports **PDF**, **DOCX**, and **TXT** files and performs custom parsing, chunking, and vector embedding with LangChain and HuggingFace.

---

## Features

- Upload and parse PDF, DOCX, and plain text documents
- Chunking and text preprocessing
- Semantic search using vector embeddings
- LLM-powered question answering
- Built using:
  - **React** (frontend)
  - **FastAPI** (backend)
  - **LangChain** for chaining logic
  - **Hugging Face** for open-source embeddings (e.g., `all-MiniLM-L6-v2`)
  - **Google Gemini** LLM via `langchain-google-genai`

---

## Demo

Watch a walkthrough of the application in action:
[Document Q&A Demo](https://drive.google.com/file/d/1gjC0WSq51h4Us7zwBcomWUK6u6rTKE6r/view?usp=drive_link)

---

## Project Purpose

This project is a personal initiative built to:

- Demonstrate practical understanding of LLMs, vector search, and document processing
- Showcase full-stack development capabilities using React and FastAPI
- Experiment with open-source NLP tools like Hugging Face and LangChain

**Note:** This is a licensed project intended for portfolio/demo purposes only. Please do not repurpose or redistribute commercially without permission.

---

## Getting Started

### Prerequisites

- Python 3.9 or later (preferably 3.11)
- Node.js 16 or later
- A Google API key (for Gemini usage)
- `poetry` or `pip` for dependency management

---

## Backend Setup (FastAPI)

### 1. Clone the repo:

```bash
git clone https://github.com/Ekuaappiah/doc-savvy-llm.git
cd doc-savvy-llm
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Backend

```bash
uvicorn main:app --reload --port 8080
```

## Frontend Setup (React)

### Install Dependencies

```bash
cd frontend
npm install
npm start
```

The React app will run on http://localhost:3000.

---

## Configuration

### .env File

Create a `.env` file in your backend root:

```ini
GOOGLE_API_KEY=your_google_api_key
```

You can generate a Gemini API key from Google AI Studio.

---

## Tech Stack

| Layer | Tool/Library |
|-------|-------------|
| Frontend | React |
| Backend | FastAPI, Uvicorn |
| LLM | Google Gemini |
| Embedding | Hugging Face (Open Source) |
| Vector DB | Chroma (local persistent) |
| Parsing | PyMuPDF, python-docx |
| Chunking | LangChain |

---

## Poetry Setup

If you're using Poetry, here's a snippet for `pyproject.toml`:

```toml
[tool.poetry.dependencies]
python = "3.11.0"
langchain = "*"
langchain-core = "*"
langchain-community = "*"
faiss-cpu = "*"
tiktoken = "*"
pymupdf = "*"
python-docx = "*"
chromadb = "*"
streamlit = "*"
fastapi = "*"
python-dotenv = "*"
pandas = "*"
langchain-google-genai = "*"
fitz = "*"
pdfminer = "*"
unstructured = "*"
sentence-transformers = "*"
langchain-chroma = "*"
langchain-huggingface = "*"
uvicorn = "*"
python-multipart = "*"
```

---

## License

This project is under a license for educational and personal demonstration purposes only.

All third-party libraries (e.g., Hugging Face models) are used under their respective open source licenses.

---

## Author

Built by @EkuaAppiah

---

## Medium Blog (Coming Soon)

A full Medium article will be published soon to explain the architecture, challenges, and design decisions behind this project.