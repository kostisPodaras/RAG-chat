from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Chat Models
class ChatSessionCreate(BaseModel):
    title: str

class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ChatMessageCreate(BaseModel):
    session_id: int
    content: str

class SourceReference(BaseModel):
    filename: str
    page: int
    content: str

class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    sources: Optional[List[SourceReference]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Document Models
class DocumentUploadResponse(BaseModel):
    filename: str
    pages: int
    message: str

class DocumentListResponse(BaseModel):
    filename: str
    upload_date: datetime
    pages: int
    size_mb: float

# Health Check
class HealthResponse(BaseModel):
    status: str
    services: dict
    timestamp: datetime