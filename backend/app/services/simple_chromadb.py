import httpx
import json
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings

class SimpleChromaDB:
    """ChromaDB client using the official Python client library"""
    
    def __init__(self):
        self.base_url = settings.chroma_url
        self.collection_name = settings.chroma_collection_name
        # Use Python client instead of HTTP API
        self.client = chromadb.HttpClient(
            host=settings.chroma_url.replace('http://', '').replace('https://', '').split(':')[0],
            port=int(settings.chroma_url.split(':')[-1]),
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )
        self.collection = None
    
    async def ensure_collection_exists(self) -> bool:
        """Ensure the collection exists, create if it doesn't"""
        try:
            # Try to get existing collection
            self.collection = self.client.get_collection(name=self.collection_name)
            return True
        except Exception as e:
            try:
                # Create collection if it doesn't exist
                print(f"Creating collection '{self.collection_name}'")
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Document embeddings for RAG"}
                )
                return True
            except Exception as create_error:
                print(f"Error creating collection: {create_error}")
                return False
    
    async def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> bool:
        """Add documents to collection"""
        if not await self.ensure_collection_exists():
            print("Failed to ensure collection exists")
            return False
            
        try:
            print(f"Adding {len(documents)} documents to ChromaDB collection")
            print(f"Sample IDs: {ids[:2] if ids else []}")
            
            # Use the Python client to add documents
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print("Successfully added documents to ChromaDB")
            return True
            
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
            return False
    
    async def query_documents(self, query_text: str, n_results: int = 5) -> Dict[str, Any]:
        """Query documents from collection"""
        if not await self.ensure_collection_exists():
            return {'documents': [[]], 'metadatas': [[]]}
            
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Error querying ChromaDB: {e}")
            return {'documents': [[]], 'metadatas': [[]]}
    
    async def delete_documents(self, ids: List[str]) -> bool:
        """Delete documents from collection"""
        if not await self.ensure_collection_exists():
            return False
            
        try:
            self.collection.delete(ids=ids)
            return True
        except Exception as e:
            print(f"Error deleting documents from ChromaDB: {e}")
            return False
    
    async def get_documents_by_metadata(self, where: Dict[str, Any]) -> Dict[str, Any]:
        """Get documents by metadata filter"""
        if not await self.ensure_collection_exists():
            return {'ids': [], 'documents': [], 'metadatas': []}
            
        try:
            results = self.collection.get(where=where)
            return results
        except Exception as e:
            print(f"Error getting documents from ChromaDB: {e}")
            return {'ids': [], 'documents': [], 'metadatas': []}