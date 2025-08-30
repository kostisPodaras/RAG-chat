from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
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
    """Upload and process a PDF document"""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
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
        
        # Process document with PyMuPDF
        doc = fitz.open(file_path)
        pages = len(doc)
        
        # Extract text and add to vector database
        await doc_service.process_document(file_path, file.filename)
        
        doc.close()
        
        return DocumentUploadResponse(
            filename=file.filename,
            pages=pages,
            message=f"Document uploaded and processed successfully. {pages} pages indexed."
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
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(settings.upload_dir, filename)
            stat = os.stat(file_path)
            
            # Get page count
            try:
                doc = fitz.open(file_path)
                pages = len(doc)
                doc.close()
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