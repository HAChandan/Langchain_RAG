
# 🤖 LangChain RAG Chatbot (FastAPI + Streamlit)

A fully functional Retrieval-Augmented Generation (RAG) chatbot built with **LangChain**, powered by **LLMs from Groq**, using **Chroma** for vector storage, and wrapped with a **FastAPI backend** and a **Streamlit frontend**.

Upload documents (`.pdf`, `.docx`, `.html`), ask questions, and get LLM answers grounded in your content — with session tracking and document management.

---

## 🚀 Features

- 📄 Upload & index documents (PDF, DOCX, HTML)
- 🔍 Retrieval-Augmented Generation with LangChain
- 🧠 Supports multiple models (e.g., LLaMA 70B, 8B)
- 💬 Chat interface with session-based history
- 📁 Document storage and management
- 🔧 FastAPI backend for API logic
- 🖼️ Streamlit UI for user interaction

---

## 🗂️ Project Structure

```
Langchain_RAG/
│
├── api/                   # FastAPI backend
│   ├── main.py            # FastAPI routes
│   ├── langchain_utils.py # Core RAG logic (chains, prompts)
│   ├── chroma_utils.py    # Vector DB logic (Chroma, embeddings)
│   ├── db_utils.py        # SQLite for chat logs and docs
│   ├── pydantic_models.py # Request/response models
│
├── app/                   # Streamlit frontend
│   ├── streamlit_app.py   # Entry point for UI
│   ├── sidebar.py         # Sidebar for upload, model, doc control
│   ├── chat_interface.py  # Chat message handling
│   ├── api_utils.py       # API calls from frontend
│
├── req.txt                # Frozen requirements
├── requirements.txt       # Python dependencies
├── .env                   # API keys (GROQ, etc.)
└── README.md              # Project documentation
```

---

## ⚙️ Requirements

- Python 3.10+
- pip (`pip install -r requirements.txt`)
- GROQ API key (for LLMs)

---

## 🛠️ Setup Instructions

1. **Clone the Repo**
```bash
git clone https://github.com/HAChandan/Langchain_RAG.git
cd Langchain_RAG
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file in `/api`**
```env
GROQ_API_KEY="your_groq_key_here"
```

---


## 📦 Dependency Note

## 🔄 If you face any issues with version conflicts, try installing from the frozen list instead:

If requirements.txt fails to install or has version conflicts, delete the old environment and create new environment and you can try installing exact pinned versions using the pre-generated req.txt file:
```bash
pip install -r req.txt
```

---

## 🧪 How to Run the App

> 💡 Open **two terminals** in the project root directory

---

### 1️⃣ Terminal 1 – Run FastAPI Backend

```bash
cd api
uvicorn main:app --reload
```

This will start the backend server at `http://localhost:8000`.

---

### 2️⃣ Terminal 2 – Run Streamlit Frontend

```bash
cd app
streamlit run streamlit_app.py
```

This will open the chatbot UI in your browser at `http://localhost:8501`.

---

## 🧪 Example Flow

1. Choose a model from the sidebar (LLaMA 70B / 8B)
2. Upload a document (`.pdf`, `.docx`, `.html`)
3. Ask questions about the document
4. View answers with full trace (model, session ID, etc.)
5. Delete documents and refresh list from sidebar

---

## 📚 API Endpoints (FastAPI)

| Method | Endpoint         | Description                         |
|--------|------------------|-------------------------------------|
| POST   | `/chat`          | Get document-grounded LLM response |
| POST   | `/upload-doc`    | Upload & index document             |
| GET    | `/list-docs`     | List all uploaded documents         |
| POST   | `/delete-doc`    | Delete a document by ID             |

---

## 📌 Notes

- Vector store is persisted in `chroma_db/`
- Uploaded files are not stored; only vector embeddings and metadata
- Chat logs are stored in SQLite (`rag_app.db`)
- Ensure `.env` is not pushed to public repos

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Groq LLMs](https://groq.com/)
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
