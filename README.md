🗂️ RAG Chat App (Private & Secure)

This project is a Retrieval-Augmented Generation (RAG) chat application designed for environments where privacy and data security are critical (e.g. law firms, medical practices).

Users can:

Upload PDF documents.

Ask natural language questions.

Receive answers along with clickable references to the original file/page.

Keep a chat history in a sidebar, similar to ChatGPT.

⚠️ Privacy-first: All models and databases run locally. No third-party API calls are made.

🛠 Tech Stack

Frontend

React + Tailwind (chat UI, sidebar, file upload)

Native fetch for API calls

Backend

Python FastAPI (API server)

LangChain
for retrieval pipeline

PyMuPDF
for PDF parsing

ChromaDB
(local vector DB)

LLM

Self-hosted via Ollama
(e.g., Llama 3, Mistral)

Database

SQLite (for chat history)

ChromaDB for embeddings

🚀 Features

✅ Secure document ingestion (manual PDF uploads)

✅ Ask natural language questions

✅ Get answers with file + page references

✅ Chat history sidebar

✅ Fully local & private (no external API calls)
