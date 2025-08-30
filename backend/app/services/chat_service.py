import chromadb
from chromadb.config import Settings as ChromaSettings
import httpx
from typing import List, Tuple
import json

from app.core.config import settings
from app.models.schemas import SourceReference

class ChatService:
    def __init__(self):
        # Initialize ChromaDB client
        self.chroma_client = chromadb.HttpClient(
            host=settings.chroma_url.replace('http://', '').split(':')[0],
            port=int(settings.chroma_url.split(':')[-1]),
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )
        
        # Get collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=settings.chroma_collection_name
            )
        except:
            # Create empty collection if it doesn't exist
            self.collection = self.chroma_client.create_collection(
                name=settings.chroma_collection_name,
                metadata={"description": "Document embeddings for RAG"}
            )
    
    async def get_response(self, user_question: str) -> Tuple[str, List[SourceReference]]:
        """Get AI response using RAG pipeline"""
        
        # Step 1: Retrieve relevant documents
        try:
            results = self.collection.query(
                query_texts=[user_question],
                n_results=5  # Get top 5 most relevant chunks
            )
        except Exception as e:
            # If no documents or query fails, proceed without context
            results = {'documents': [[]], 'metadatas': [[]]}
        
        # Step 2: Prepare context and sources
        context = ""
        sources = []
        
        if results['documents'] and results['documents'][0]:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            
            for i, (doc, metadata) in enumerate(zip(documents, metadatas)):
                context += f"Source {i+1} (from {metadata['filename']}, page {metadata['page']}):\n{doc}\n\n"
                
                sources.append(SourceReference(
                    filename=metadata['filename'],
                    page=metadata['page'],
                    content=doc[:200] + "..." if len(doc) > 200 else doc
                ))
        
        # Step 3: Create prompt for Ollama
        if context:
            prompt = f"""Based on the following context from uploaded documents, please answer the user's question. If the context doesn't contain relevant information, say so and provide a general response.

Context:
{context}

User Question: {user_question}

Please provide a helpful answer and reference which sources you used:"""
        else:
            prompt = f"""No documents have been uploaded yet or no relevant information was found. Please provide a general response to this question:

{user_question}"""
        
        # Step 4: Get response from Ollama
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.ollama_url}/api/generate",
                    json={
                        "model": settings.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "max_tokens": 1000
                        }
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get('response', 'Sorry, I could not generate a response.')
                else:
                    ai_response = "Sorry, the AI service is currently unavailable."
                    
        except Exception as e:
            ai_response = f"Error communicating with AI service: {str(e)}"
        
        return ai_response, sources if context else []