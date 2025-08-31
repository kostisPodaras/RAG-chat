from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import List
import os
import aiofiles
from datetime import datetime
import fitz  # PyMuPDF

from app.core.config import settings
from app.models.schemas import DocumentUploadResponse, DocumentListResponse
from app.services.document_service import DocumentService

router = APIRouter()

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    doc_service: DocumentService = Depends(DocumentService)
):
    """Upload and process a document (PDF or TXT)"""
    
    # Validate file type
    filename_lower = file.filename.lower()
    if not (filename_lower.endswith('.pdf') or filename_lower.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are allowed")
    
    # Validate file size
    file_size_mb = len(await file.read()) / (1024 * 1024)
    await file.seek(0)  # Reset file pointer
    
    if file_size_mb > settings.max_file_size_mb:
        raise HTTPException(
            status_code=400, 
            detail=f"File size exceeds {settings.max_file_size_mb}MB limit"
        )
    
    # Save file
    file_path = os.path.join(settings.upload_dir, file.filename)
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Process document and get page count
        if filename_lower.endswith('.pdf'):
            # For PDF files, get page count with PyMuPDF
            doc = fitz.open(file_path)
            pages = len(doc)
            doc.close()
        else:
            # For TXT files, treat as 1 page
            pages = 1
        
        # Extract text and add to vector database
        await doc_service.process_document(file_path, file.filename)
        
        return DocumentUploadResponse(
            filename=file.filename,
            pages=pages,
            message=f"Document uploaded and processed successfully. {pages} {'page' if pages == 1 else 'pages'} indexed."
        )
        
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.get("/documents", response_model=List[DocumentListResponse])
async def list_documents():
    """List all uploaded documents"""
    documents = []
    
    if not os.path.exists(settings.upload_dir):
        return documents
    
    for filename in os.listdir(settings.upload_dir):
        filename_lower = filename.lower()
        if filename_lower.endswith('.pdf') or filename_lower.endswith('.txt'):
            file_path = os.path.join(settings.upload_dir, filename)
            stat = os.stat(file_path)
            
            # Get page count
            try:
                if filename_lower.endswith('.pdf'):
                    doc = fitz.open(file_path)
                    pages = len(doc)
                    doc.close()
                else:
                    # TXT files have 1 page
                    pages = 1
            except:
                pages = 0
            
            documents.append(DocumentListResponse(
                filename=filename,
                upload_date=datetime.fromtimestamp(stat.st_mtime),
                pages=pages,
                size_mb=stat.st_size / (1024 * 1024)
            ))
    
    return sorted(documents, key=lambda x: x.upload_date, reverse=True)

@router.delete("/documents/{filename}")
async def delete_document(
    filename: str,
    doc_service: DocumentService = Depends(DocumentService)
):
    """Delete a document and remove from vector database"""
    file_path = os.path.join(settings.upload_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Remove from vector database
        await doc_service.delete_document(filename)
        
        # Remove file
        os.remove(file_path)
        
        return {"message": f"Document {filename} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@router.get("/documents/view/{filename}")
async def view_document(filename: str):
    """Serve a document file for viewing in browser"""
    # Security: Only allow alphanumeric, dots, dashes, and underscores in filename
    import re
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_path = os.path.join(settings.upload_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check file extension
    filename_lower = filename.lower()
    if not (filename_lower.endswith('.pdf') or filename_lower.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files can be viewed")
    
    try:
        # Set appropriate media type
        media_type = "application/pdf" if filename_lower.endswith('.pdf') else "text/plain"
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type=media_type,
            headers={
                "Content-Disposition": "inline",  # Display in browser instead of download
                "Cache-Control": "private, max-age=3600",  # Cache for 1 hour
                "X-Frame-Options": "SAMEORIGIN",  # Allow iframe from same origin
                "Content-Security-Policy": "frame-ancestors 'self' http://localhost:3000"  # Allow iframe from frontend
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving document: {str(e)}")