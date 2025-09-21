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

PostgreSQL (for chat history)

ChromaDB for embeddings

🚀 Features

✅ Secure document ingestion (manual PDF uploads)

✅ Ask natural language questions

✅ Get answers with file + page references

✅ Chat history sidebar

✅ Fully local & private (no external API calls)

## 🚀 Quick Start for Developers

### Prerequisites

- **Docker & Docker Compose** (for containerized services)
- **Node.js 18+** (for frontend development)
- **Python 3.11+** (for backend development)
- **Git** (for version control)

### Step 1: Clone the Repository

```bash
git clone https://github.com/kostisPodaras/RAG-chat.git
cd RAG-chat
```

### Step 2: Install Ollama and Download LLM

**Install Ollama:**

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

**Download the LLM model (required):**

```bash
ollama pull llama3.2:3b
```

**Verify installation:**

```bash
ollama list
# Should show llama3.2:3b
```

### Step 3: Start All Services

**Development mode with hot reload:**

```bash
docker-compose up
```

### Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **ChromaDB**: http://localhost:8000
- **Ollama**: http://localhost:11434

### Step 5: Verify Everything Works

1. **Check health status**: Visit http://localhost:8001/api/v1/health
2. **Upload a PDF**: Use the upload button in the UI
3. **Ask a question**: Type a question about your uploaded document
4. **Check responses**: Verify you get answers with source references

## 🛠️ Development Workflow

### Frontend Development

```bash
cd frontend
npm install
npm start  # Development server on port 3000
npm test   # Run tests
npm run build  # Production build
```

### Backend Development

```bash
cd backend
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
pytest  # Run tests
```

### Database Management

**PostgreSQL** is used for chat history. The database is automatically initialized when you start the services.

**ChromaDB** stores document embeddings and is also auto-initialized.

## 📁 Project Structure

```
RAG-chat/
├── frontend/          # React + TypeScript UI
├── backend/           # FastAPI Python server
├── docker-compose.yml # All services configuration
├── CLAUDE.md         # Development guidelines
├── FLOW.md           # Application flow documentation
└── TODO.md           # Current tasks and features
```

## ⚙️ Configuration

Environment variables are managed in `backend/app/core/config.py`:

- `OLLAMA_URL`: Ollama service endpoint (default: http://ollama:11434)
- `OLLAMA_MODEL`: LLM model name (default: llama3.2:3b)
- `CHROMA_URL`: ChromaDB endpoint (default: http://chromadb:8000)
- `DATABASE_URL`: PostgreSQL connection string
- `MAX_FILE_SIZE_MB`: Maximum upload size (default: 50MB)

## 🔧 Troubleshooting

### Common Issues

**1. Ollama model not found:**

```bash
# Download the model
ollama pull llama3.2:3b
```

**2. Port conflicts:**

```bash
# Check what's using the ports
lsof -i :3000  # Frontend
lsof -i :8001  # Backend
lsof -i :8000  # ChromaDB
lsof -i :11434 # Ollama
```

**3. Docker issues:**

```bash
# Clean up and restart
docker-compose down
docker system prune -f
docker-compose up --build
```

**4. Frontend not connecting to backend:**

- Verify backend is running on port 8001
- Check CORS settings in `backend/app/main.py`
- Ensure proxy is configured in `frontend/package.json`

**5. ChromaDB connection issues:**

- Wait 30 seconds after starting services for ChromaDB to initialize
- Check logs: `docker-compose logs chromadb`

### Development Tips

- Use `docker-compose up --watch` for hot reload during development
- Check service health at http://localhost:8001/api/v1/health
- View uploaded documents in the ChromaDB admin UI (if enabled)
- Monitor logs with `docker-compose logs -f [service-name]`

## 🤝 Contributing

1. Read `CLAUDE.md` for development guidelines
2. Check `TODO.md` for current tasks
3. Follow conventional commit format: `type(scope): description`
4. Update `GIT_HISTORY.md` with every commit
5. Test locally before pushing

## 📚 Documentation

- `CLAUDE.md`: Complete development guidelines and architecture
- `FLOW.md`: Detailed application flow and API examples
- `TODO.md`: Current tasks and future enhancements
