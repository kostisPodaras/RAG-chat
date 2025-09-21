# RAG Chat Application Flow

This document outlines the step-by-step flow of the RAG chat application.

## Step 1: Load Chat Sessions

**Request:**
```
GET /api/v1/chat/sessions?page=1&page_size=20
```

**API Response Example:**
```json
[
  {
    "id": 28,
    "title": "How are lost profits calculated in business disputes?",
    "created_at": "2025-08-31T20:15:48.812566",
    "updated_at": null
  },
  {
    "id": 27,
    "title": "What is Rebecca Martinez's settlement demand?",
    "created_at": "2025-08-31T20:17:28.193157",
    "updated_at": null
  }
]
```

**Purpose:** Populate the sidebar with existing chat sessions. Shows minimal session metadata needed for UI display with pagination support.

---

## Step 2: Load Chat Messages for Selected Session

**Request:**
```
GET /api/v1/chat/sessions/28/messages
```

**Alternative: Send New Message (POST)**
```
POST /api/v1/chat/sessions/28/messages
Content-Type: application/json

{
  "session_id": 28,
  "content": "What are the key points in Rebecca Martinez's case?"
}
```

**API Response Example:**
```json
[
  {
    "id": 145,
    "session_id": 28,
    "role": "user",
    "content": "How are lost profits calculated in business disputes?",
    "sources": null,
    "created_at": "2025-08-31T20:15:48.825134"
  },
  {
    "id": 146,
    "session_id": 28,
    "role": "assistant",
    "content": "Lost profits in business disputes are typically calculated using several methodologies:\n\n1. **Before-and-After Method**: Compares actual performance to historical performance before the alleged harm.\n\n2. **Yardstick Method**: Uses comparable businesses or market benchmarks as a baseline for expected performance.\n\n3. **But-For Analysis**: Determines what would have happened 'but for' the defendant's actions.\n\nKey factors considered include:\n- Historical financial performance\n- Market conditions and trends\n- Causation between the alleged harm and losses\n- Mitigation efforts by the plaintiff\n\nExperts often discount future profits to present value and must demonstrate reasonable certainty in their calculations.",
    "sources": [
      {
        "filename": "client_002_david_kim.pdf",
        "page": 0,
        "content": "break violations (Labor Code 226.7), inaccurate wage statements (Labor Code 226). DAMAGES: 18\nmonths unpaid overtime estimated at $45,000, meal/rest break premiums $8,400, waiting time\npenalties, attorney's fees. PAGA penalties potentially available.\nCASE TIMELINE\n Initial incident/violation occurr..."
      },
      {
        "filename": "client_005_sarah_chen.pdf",
        "page": 0,
        "content": "CONFIDENTIAL ATTORNEY-CLIENT PRIVILEGED\nCLIENT FILE: SARAH CHEN\nClient ID:\nLAW-005\nFull Name:\nSarah Chen\nPhone:\n(619) 555-0567\nEmail:\nsarah.chen.cto@email.com\nAddress:\n1647 Sunset Boulevard, San Diego, CA 92103\nEmployer/Defendant:\nFormer employer: InnovateTech Systems\nCase Type:\nTrade Secret Misappr..."
      },
      {
        "filename": "legal_reference.pdf",
        "page": 5,
        "content": "legal basis for processing  DATA MINIMIZATION: Collect only necessary information  CONSENT:\nMust be freely given, specific, informed  BREACH NOTIFICATION: Must notify within 72 hours  DATA\nSUBJECT RIGHTS: Access, rectification, erasure, portability Maximum fines: 4% of annual revenue or\n€20 mill..."
      }
    ],
    "created_at": "2025-08-31T20:15:52.441298"
  }
]
```

**Purpose:** 
- **GET**: Load the full conversation history when user selects a specific chat session
- **POST**: Send a new message and get AI response via RAG pipeline

**Note:** Both GET and POST methods return the same message structure. The POST method returns the newly created AI response message after processing through the RAG pipeline (ChromaDB → Ollama → response with sources).

---

---

## Step 3: Health Check Monitoring

**Request:**
```
GET /api/v1/health
```

**API Response Example:**
```json
{
  "status": "healthy",
  "services": {
    "ollama": "healthy",
    "chromadb": "healthy"
  },
  "timestamp": "2025-08-31T23:45:12.123456"
}
```

**Purpose:** Monitors all critical services (Ollama LLM, ChromaDB vector database) to ensure the RAG pipeline is functional. Frontend automatically checks every 30 seconds and displays system status in the top bar.

**Status Types:**
- `healthy`: All services operational
- `degraded`: Some services down, limited functionality
- `unhealthy`: Critical services unavailable

**Behind the Scenes:**
- Ollama check: `GET {ollama_url}/api/tags` (5s timeout)
- ChromaDB check: `GET {chroma_url}/api/v1/heartbeat` (5s timeout)
- Visual indicator: Color-coded dot in UI (🟢🟡🔴⚫)

---

---

## Step 4: View Document File

**Request:**
```
GET /api/v1/documents/view/client_005_sarah_chen.pdf
```

**API Response:**
```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: inline; filename="client_005_sarah_chen.pdf"
Cache-Control: private, max-age=3600
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: frame-ancestors 'self' http://localhost:3000

[Binary PDF file content]
```

**Purpose:** Serves the actual uploaded document file for viewing in browser. Users can click on source references in chat responses to view the original document.

**Security Features:**
- Filename validation (alphanumeric, dots, dashes, underscores only)
- File type restriction (PDF/TXT only)
- Same-origin iframe protection
- Private caching (1 hour)

**Usage:** 
- Embedded in `<iframe>` for inline viewing
- Opened in new tab/window
- Referenced from chat message sources

---

## Database Architecture: ORM Explanation

### What is SQLAlchemy (Our ORM)?

**ORM = Object-Relational Mapping** - Yes, it's like a **framework for databases** that converts Python objects into SQL operations.

**Without ORM (Raw SQL):**
```python
# Hard to write, error-prone
cursor.execute("SELECT * FROM chat_sessions WHERE user_id = ?", (user_id,))
rows = cursor.fetchall()
```

**With ORM (SQLAlchemy):**
```python
# Clean, readable Python code
sessions = db.query(ChatSession).filter(ChatSession.user_id == user_id).all()
```

### Key Benefits in Our App

1. **No SQL needed** - Write Python instead of SQL queries
2. **Type safety** - IDE knows what fields exist (`session.title`, `session.id`)
3. **Database agnostic** - Same code works with PostgreSQL, SQLite, MySQL
4. **Automatic mapping** - Python objects ↔ Database tables

### Our Models (`/backend/app/core/database.py`)

- `ChatSession` Python class = `chat_sessions` PostgreSQL table
- `ChatMessage` Python class = `chat_messages` PostgreSQL table

**Example from our codebase:**
```python
# Create session (becomes INSERT INTO chat_sessions...)
session = ChatSession(title="New Chat")
db.add(session)
db.commit()

# Query sessions (becomes SELECT * FROM chat_sessions ORDER BY...)
sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
```

**Bottom line:** ORM = Database framework that lets you write Python objects instead of SQL strings.

---

## Next Steps (To Be Added)
- Step 5: Document upload flow
- Step 6: New message/RAG processing