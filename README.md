# rag-agentic-ai-chatbot
RAG-based AI Chatbot using LangGraph, ChromaDB and FastAPI

Project Overview

A Retrieval-Augmented Generation (RAG) chatbot built using LangGraph, ChromaDB, HuggingFace embeddings, FastAPI, and OpenRouter. The chatbot answers questions strictly from the "Agentic AI" eBook by retrieving relevant document chunks before generating responses.

Features
PDF ingestion
Automatic chunkingav
SentenceTransformer embeddings
ChromaDB vector database
LangGraph workflow
FastAPI REST API
OpenRouter LLM integration
Source chunk retrieval
Confidence score
Tech Stack
Python
FastAPI
LangGraph
ChromaDB
HuggingFace
OpenRouter
Sentence Transformers


```git clone ... ```
```python -m venv venv```
```pip install -r requirements.txt```
```python -m scripts.build_vectordb```
```uvicorn app.main:app --reload```
