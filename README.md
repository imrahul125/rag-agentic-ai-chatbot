# 🤖 Agentic AI RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot built with **Python, LangGraph, ChromaDB, HuggingFace Embeddings, FastAPI, and OpenRouter LLM**. The chatbot answers user questions **strictly based on the Agentic AI eBook** by retrieving relevant document chunks before generating responses.

## 📌 Features

- 📖 PDF ingestion and text extraction
- ✂️ Automatic document chunking
- 🧠 Sentence Transformer embeddings
- 🗂️ ChromaDB vector database
- 🔍 Semantic similarity search
- 🔄 LangGraph workflow
- 💬 OpenRouter LLM integration
- 🚀 FastAPI REST API
- 📚 Source chunk retrieval
- 📊 Confidence score with every response
- ❌ Prevents answering questions outside the provided document

---

# 🏗️ Architecture

```
                Agentic AI eBook (PDF)
                         │
                         ▼
               PDF Text Extraction
                         │
                         ▼
                 Text Chunking
                         │
                         ▼
             HuggingFace Embeddings
                         │
                         ▼
                  ChromaDB Storage
                         │
                         ▼
               Similarity Retrieval
                         │
                         ▼
                 LangGraph Workflow
                         │
                         ▼
              OpenRouter Large Language Model
                         │
                         ▼
                FastAPI REST API Response
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| FastAPI | REST API |
| LangGraph | Workflow orchestration |
| ChromaDB | Vector Database |
| HuggingFace | Embeddings |
| Sentence Transformers | Embedding Model |
| OpenRouter | LLM |
| PyPDF | PDF Parsing |

---

# 📂 Project Structure

```
rag-agentic-ai-chatbot/
│
├── app/
│   ├── api/
│   │   ├── models.py
│   │   └── routes.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   └── workflow.py
│   │
│   ├── services/
│   │   ├── embeddings.py
│   │   ├── ingest.py
│   │   ├── llm.py
│   │   ├── rag.py
│   │   ├── retriever.py
│   │   └── vectordb.py
│   │
│   ├── config.py
│   ├── main.py
│   └── __init__.py
│
├── data/
│   └── Ebook-Agentic-AI.pdf
│
├── scripts/
│   ├── build_vectordb.py
│   ├── test_graph.py
│   ├── test_ingest.py
│   ├── test_llm.py
│   └── test_retriever.py
│
├── vectorstore/
├── requirements.txt
├── README.md
└── .env
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/imrahul125/rag-agentic-ai-chatbot.git
```

```bash
cd rag-agentic-ai-chatbot
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Create Environment File

Create a file named **.env**

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

---

## 5️⃣ Add the PDF

Place the provided eBook inside

```
data/
```

Example:

```
data/Ebook-Agentic-AI.pdf
```

---

## 6️⃣ Build the Vector Database

```bash
python -m scripts.build_vectordb
```

Expected output

```
Stored 119 chunks.
```

---

## 7️⃣ Run the API

```bash
uvicorn app.main:app --reload
```

---

## 8️⃣ Open Swagger UI

Open

```
http://127.0.0.1:8000/docs
```

---

# 💬 Example Request

```json
{
  "question": "What is Agentic AI?"
}
```

---

# ✅ Example Response

```json
{
  "answer": "Agentic AI refers to AI systems capable of autonomous reasoning, planning, and decision-making based on the provided document.",
  "confidence": 0.63,
  "sources": [
    {
      "score": 0.63,
      "text": "Agentic AI is..."
    }
  ]
}
```

---

# 📋 Sample Questions

- What is Agentic AI?
- What are Multi-Agent Systems?
- What are the applications of Agentic AI?
- What are the benefits of Agentic AI?
- How does Agentic AI differ from traditional AI?
- What are the components of an Agentic AI system?

---

# 🔍 API Endpoints

## Health Check

```
GET /
```

Returns

```json
{
  "message": "Agentic AI RAG Chatbot is running!"
}
```

---

## Chat Endpoint

```
POST /chat
```

Request

```json
{
  "question": "What is Agentic AI?"
}
```

---

# 🧠 How It Works

1. Load the Agentic AI PDF.
2. Split the document into smaller chunks.
3. Generate embeddings using Sentence Transformers.
4. Store embeddings inside ChromaDB.
5. Retrieve the most relevant chunks using semantic search.
6. Pass the retrieved context into the LangGraph workflow.
7. Generate grounded answers using OpenRouter LLM.
8. Return:
   - Final Answer
   - Confidence Score
   - Retrieved Context

---

# 📦 Dependencies

Major libraries used:

- FastAPI
- Uvicorn
- LangGraph
- ChromaDB
- HuggingFace
- Sentence Transformers
- OpenRouter
- PyPDF
- Python Dotenv

---

# 📄 License

This project was developed as part of the AI Engineer Internship technical assessment.

The knowledge base used is the publicly available **Agentic AI eBook**.

---

# 👨‍💻 Author

**Rahul Bhagwat**

GitHub: https://github.com/imrahul125

---

## ⭐ If you found this project useful, consider giving it a star.
