import httpx
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings

class SimpleChromaDB:
    """Simple ChromaDB client using direct HTTP requests to bypass v1/v2 API issues"""
    
    def __init__(self):
        self.base_url = settings.chroma_url
        self.collection_name = settings.chroma_collection_name
    
    async def ensure_collection_exists(self) -> bool:
        """Ensure the collection exists, create if it doesn't"""
        async with httpx.AsyncClient() as client:
            try:
                # Try to get collection first
                response = await client.get(f"{self.base_url}/api/v1/collections/{self.collection_name}")
                return response.status_code == 200
            except:
                # Try to create collection
                try:
                    response = await client.post(
                        f"{self.base_url}/api/v1/collections",
                        json={
                            "name": self.collection_name,
                            "metadata": {"description": "Document embeddings for RAG"}
                        }
                    )
                    return response.status_code in [200, 201]
                except:
                    return False
    
    async def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> bool:
        """Add documents to collection"""
        if not await self.ensure_collection_exists():
            return False
            
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "documents": documents,
                    "metadatas": metadatas,
                    "ids": ids
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/collections/{self.collection_name}/add",
                    json=payload,
                    timeout=30.0
                )
                
                return response.status_code in [200, 201]
            except Exception as e:
                print(f"Error adding documents to ChromaDB: {e}")
                return False
    
    async def query_documents(self, query_text: str, n_results: int = 5) -> Dict[str, Any]:
        """Query documents from collection"""
        if not await self.ensure_collection_exists():
            return {'documents': [[]], 'metadatas': [[]]}
            
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "query_texts": [query_text],
                    "n_results": n_results
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/collections/{self.collection_name}/query",
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {'documents': [[]], 'metadatas': [[]]}
                    
            except Exception as e:
                print(f"Error querying ChromaDB: {e}")
                return {'documents': [[]], 'metadatas': [[]]}
    
    async def delete_documents(self, ids: List[str]) -> bool:
        """Delete documents from collection"""
        if not await self.ensure_collection_exists():
            return False
            
        async with httpx.AsyncClient() as client:
            try:
                payload = {"ids": ids}
                
                response = await client.post(
                    f"{self.base_url}/api/v1/collections/{self.collection_name}/delete",
                    json=payload,
                    timeout=30.0
                )
                
                return response.status_code in [200, 201]
            except Exception as e:
                print(f"Error deleting documents from ChromaDB: {e}")
                return False
    
    async def get_documents_by_metadata(self, where: Dict[str, Any]) -> Dict[str, Any]:
        """Get documents by metadata filter"""
        if not await self.ensure_collection_exists():
            return {'ids': [], 'documents': [], 'metadatas': []}
            
        async with httpx.AsyncClient() as client:
            try:
                payload = {"where": where}
                
                response = await client.post(
                    f"{self.base_url}/api/v1/collections/{self.collection_name}/get",
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {'ids': [], 'documents': [], 'metadatas': []}
                    
            except Exception as e:
                print(f"Error getting documents from ChromaDB: {e}")
                return {'ids': [], 'documents': [], 'metadatas': []}