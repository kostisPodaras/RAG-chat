from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import json

from app.core.database import get_db, ChatSession, ChatMessage
from app.models.schemas import (
    ChatSessionCreate, ChatSessionResponse,
    ChatMessageCreate, ChatMessageResponse
)
from app.services.langchain_chat_service import LangChainChatService

router = APIRouter()

@router.post("/chat/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    db_session = ChatSession(title=session_data.title)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/chat/sessions", response_model=List[ChatSessionResponse])
async def list_chat_sessions(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """List chat sessions with pagination"""
    offset = (page - 1) * page_size
    return db.query(ChatSession).order_by(
        ChatSession.updated_at.desc(),
        ChatSession.created_at.desc()
    ).offset(offset).limit(page_size).all()

@router.get("/chat/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(session_id: int, db: Session = Depends(get_db)):
    """Get messages for a specific chat session"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at).all()
    
    # Parse sources JSON
    for message in messages:
        if message.sources:
            try:
                message.sources = json.loads(message.sources)
            except:
                message.sources = None
    
    return messages

@router.post("/chat/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: int,
    message_data: ChatMessageCreate,
    db: Session = Depends(get_db),
    chat_service: LangChainChatService = Depends(LangChainChatService)
):
    """Send a message and get AI response"""
    
    # Verify session exists
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    try:
        # Save user message
        user_message = ChatMessage(
            session_id=session_id,
            role="user",
            content=message_data.content
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Get AI response with RAG
        ai_response, sources = await chat_service.get_response(message_data.content)
        
        # Save AI response
        assistant_message = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=ai_response,
            sources=json.dumps([source.dict() for source in sources]) if sources else None
        )
        db.add(assistant_message)
        
        # Update session timestamp
        session.updated_at = assistant_message.created_at
        
        db.commit()
        db.refresh(assistant_message)
        
        # Prepare response
        assistant_message.sources = sources
        return assistant_message
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.delete("/chat/sessions/{session_id}")
async def delete_chat_session(session_id: int, db: Session = Depends(get_db)):
    """Delete a chat session and all its messages"""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Delete messages first
    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    
    # Delete session
    db.delete(session)
    db.commit()
    
    return {"message": "Chat session deleted successfully"}