import chromadb
from chromadb.config import Settings as ChromaSettings
import fitz  # PyMuPDF
from typing import List
import uuid
from sentence_transformers import SentenceTransformer

from app.core.config import settings

class DocumentService:
    def __init__(self):
        # Initialize ChromaDB client
        self.chroma_client = chromadb.HttpClient(
            host=settings.chroma_url.replace('http://', '').split(':')[0],
            port=int(settings.chroma_url.split(':')[-1]),
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=settings.chroma_collection_name
            )
        except:
            self.collection = self.chroma_client.create_collection(
                name=settings.chroma_collection_name,
                metadata={"description": "Document embeddings for RAG"}
            )
    
    async def process_document(self, file_path: str, filename: str):
        """Process a PDF document and add to vector database"""
        
        # Extract text from PDF
        doc = fitz.open(file_path)
        
        documents = []
        metadatas = []
        ids = []
        
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
                ids.append(f"{filename}_{page_num}_{i}_{uuid.uuid4().hex[:8]}")
        
        doc.close()
        
        # Add to ChromaDB
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
    
    async def delete_document(self, filename: str):
        """Remove all chunks for a document from vector database"""
        # Get all document IDs for this filename
        results = self.collection.get(
            where={"filename": filename}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
    
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