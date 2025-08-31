# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a privacy-first RAG (Retrieval-Augmented Generation) chat application designed for sensitive environments like law firms and medical practices. All services run locally with no external API calls.

## Architecture

**Microservices Architecture** with 4 containerized services:

- **Frontend** (React/TypeScript) - Port 3000
- **Backend** (FastAPI/Python) - Port 8001
- **ChromaDB** (Vector Database) - Port 8000
- **Ollama** (Local LLM) - Port 11434

## Development Commands

### Docker Operations

```bash
docker-compose up --watch    # Hot reload development
docker-compose up -d         # Background services
docker-compose down         # Stop all services
docker-compose logs -f      # Follow logs
```

### Frontend Development

```bash
cd frontend
npm start                   # Development server (port 3000)
npm run build              # Production build
npm test                   # Run tests
```

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001  # Development server
pytest                     # Run tests
```

## Key Services & Architecture

### Backend (`/backend/app/`)

**FastAPI Structure**:

- `main.py` - FastAPI app entry point with CORS
- `core/config.py` - Pydantic settings with environment variables
- `core/database.py` - SQLAlchemy models (ChatSession, ChatMessage)
- `api/endpoints/` - REST API endpoints (health, documents, chat)
- `services/` - Core business logic

**Key Services**:

- `DocumentService` - PDF/TXT processing using PyMuPDF, text chunking (500 chars), ChromaDB storage
- `ChatService` - RAG pipeline orchestration (query ChromaDB → context assembly → Ollama LLM)
- `SimpleChromaDB` - Custom HTTP client for ChromaDB v2 API compatibility

**Database Design**:

- SQLite for chat history (sessions/messages)
- ChromaDB for document embeddings with metadata (filename, page, chunk)

### Frontend (`/frontend/src/`)

**React + TypeScript Structure**:

- `pages/ChatPage.tsx` - Main interface with document panel
- `components/Sidebar.tsx` - Chat session management
- `components/ChatMessage.tsx` - Message display with source references
- `components/DocumentUpload.tsx` - Drag-drop file upload with react-dropzone
- `services/api.ts` - API client with comprehensive error handling

**UI Framework**: TailwindCSS with custom `rag-*` color palette, Headless UI components

## RAG Pipeline Flow

1. **Document Ingestion**: Upload → PyMuPDF extraction → Text chunking → ChromaDB storage
2. **Query Processing**: User question → ChromaDB similarity search → Top 5 relevant chunks
3. **Response Generation**: Context assembly → Ollama prompt → LLM response with source attribution

## Configuration

**Environment Variables** (managed via `backend/app/core/config.py`):

```bash
OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b
CHROMA_URL=http://chromadb:8000
DATABASE_URL=sqlite:///./data/chat_history.db
MAX_FILE_SIZE_MB=50
```

## API Structure

**REST Endpoints**:

- `GET /api/v1/health` - Multi-service health checks
- `POST /api/v1/documents/upload` - File upload with validation
- `GET /api/v1/documents` - List uploaded documents
- `DELETE /api/v1/documents/{filename}` - Remove document
- `POST /api/v1/chat/sessions` - Create chat session
- `GET /api/v1/chat/sessions/{id}/messages` - Message history
- `POST /api/v1/chat/sessions/{id}/messages` - Send message (triggers RAG)

## Data Persistence

**Docker Volumes**:

- `ollama_data` - Ollama models and cache
- `chromadb_data` - Vector embeddings and metadata
- `uploaded_docs` - Original uploaded files
- `sqlite_data` - Chat history database

## Testing

- **Backend**: pytest with async support (`pytest-asyncio`)
- **Frontend**: Jest with React Testing Library (Create React App defaults)
- All services have health check endpoints for monitoring

## Common Issues

- **ChromaDB Compatibility**: Uses custom `SimpleChromaDB` client to work with v2 API
- **File Upload**: Max 50MB, supports PDF/TXT only
- **Frontend Proxy**: Development proxy to backend on port 8001
- **Hot Reload**: Docker compose `--watch` enables file watching for development

## Key Dependencies

**Backend**: FastAPI 0.104.1, ChromaDB 0.4.18, PyMuPDF 1.23.8, LangChain 0.0.350, SQLAlchemy 2.0.23
**Frontend**: React 18.2.0, TailwindCSS 3.3.0, Headless UI 1.7.0, react-dropzone 14.2.0

Giorgos Xonikis
11:51 π.μ.

## Development Rules

- Work on one step at a time
- Verify each step works before proceeding
- Pause for review and confirmation at each checkpoint
- Follow existing code conventions and patterns
- **IMPORTANT**: Update `GIT_HISTORY.md` with every commit (required)

## Response Protocol

- **When asked a question**: Provide recommendations and explain different approaches. DO NOT start coding.
- **When given direction**: Only after explicit instruction on which approach to use, begin implementation.
- **Analysis first**: Always analyze and discuss options before making changes.
- Example:
  - User: "How should I handle loading states?"
  - Assistant: Provides 3-4 approaches with pros/cons
  - User: "Use approach 2"
  - Assistant: Now implements the chosen approach

## Git Commit Requirements

**CRITICAL**: Three mandatory requirements for all commits:

### 1. Never Commit Without Explicit Instruction

- **NEVER** commit changes unless explicitly instructed by the user
- Wait for clear instructions like "commit this", "commit the changes", or "create a commit"
- Only push to remote when specifically asked
- The user will tell you when they want changes committed and pushed

### 2. Conventional Commits Format

- All commit messages MUST follow conventional commits format
- Format: `type(scope): subject` (scope is optional)
- Allowed types: feat, fix, docs, style, refactor, perf, test, chore, build, ci, revert
- Examples:
  - `feat: add user authentication`
  - `fix(api): resolve database timeout`
  - `docs: update README with examples`
- Enforced by commit-msg hook

### 3. GIT_HISTORY.md Updates

- The GIT_HISTORY.md file MUST be updated with every commit
- After creating a commit, immediately update with:
  - Commit hash (short form)
  - Commit type and description
  - Detailed bullet points of changes
  - Update statistics section if needed
- Enforced by pre-commit hook
- Never skip this step - it maintains project documentation
