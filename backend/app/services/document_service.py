import fitz  # PyMuPDF
from typing import List
import uuid

from app.core.config import settings
from app.services.simple_chromadb import SimpleChromaDB

class DocumentService:
    def __init__(self):
        # Initialize simple ChromaDB client
        self.chroma_client = SimpleChromaDB()
    
    async def process_document(self, file_path: str, filename: str):
        """Process a document (PDF or TXT) and add to vector database"""
        
        documents = []
        metadatas = []
        ids = []
        
        # Determine file type and extract text
        if filename.lower().endswith('.pdf'):
            # Extract text from PDF
            doc = fitz.open(file_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                # Skip empty pages
                if not text.strip():
                    continue
                
                # Split into chunks (simple sentence-based chunking)
                chunks = self._chunk_text(text, max_length=500)
                
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({
                        "filename": filename,
                        "page": page_num + 1,
                        "chunk": i + 1
                    })
                    ids.append(str(uuid.uuid4()))
            
            doc.close()
            
        elif filename.lower().endswith('.txt'):
            # Extract text from TXT file
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if text.strip():
                # Split into chunks (simple sentence-based chunking)
                chunks = self._chunk_text(text, max_length=500)
                
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({
                        "filename": filename,
                        "page": 1,  # Text files have only one "page"
                        "chunk": i + 1
                    })
                    ids.append(str(uuid.uuid4()))
        
        # Add to ChromaDB
        if documents:
            success = await self.chroma_client.add_documents(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            if not success:
                raise Exception("Failed to add documents to ChromaDB")
    
    async def delete_document(self, filename: str):
        """Remove all chunks for a document from vector database"""
        # Get all document IDs for this filename
        results = await self.chroma_client.get_documents_by_metadata(
            where={"filename": filename}
        )
        
        if results['ids']:
            success = await self.chroma_client.delete_documents(ids=results['ids'])
            if not success:
                raise Exception("Failed to delete documents from ChromaDB")
    
    def _chunk_text(self, text: str, max_length: int = 500) -> List[str]:
        """Simple text chunking by sentences"""
        sentences = text.replace('\n', ' ').split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) > max_length and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
            else:
                current_chunk += sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if chunk.strip()]