import httpx
from typing import List, Tuple
import json

from app.core.config import settings
from app.models.schemas import SourceReference
from app.services.simple_chromadb import SimpleChromaDB

class ChatService:
    def __init__(self):
        # Initialize simple ChromaDB client
        self.chroma_client = SimpleChromaDB()
    
    async def get_response(self, user_question: str) -> Tuple[str, List[SourceReference]]:
        """Get AI response using RAG pipeline"""
        
        # Step 1: Retrieve relevant documents
        try:
            results = await self.chroma_client.query_documents(
                query_text=user_question,
                n_results=5,  # Increase to 5 for better coverage of general queries
                similarity_threshold=0.25  # Lower threshold for better recall on pattern matching
            )
        except Exception as e:
            # If no documents or query fails, proceed without context
            results = {'documents': [[]], 'metadatas': [[]]}
        
        # Step 2: Prepare context and sources
        context = ""
        all_sources = []
        
        if results['documents'] and results['documents'][0]:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            
            for i, (doc, metadata) in enumerate(zip(documents, metadatas)):
                context += f"Source {i+1} (from {metadata['filename']}, page {metadata['page']}):\n{doc}\n\n"
                
                all_sources.append({
                    'source': SourceReference(
                        filename=metadata['filename'],
                        page=metadata['page'],
                        content=doc[:200] + "..." if len(doc) > 200 else doc
                    ),
                    'full_content': doc,
                    'metadata': metadata
                })
        
        # Step 3: Create prompt for Ollama
        if context:
            prompt = f"""Answer the user's question using the provided context. Only use information that directly answers their question.

Context:
{context}

User Question: {user_question}

Provide a clear, direct answer based on the relevant information."""
        else:
            prompt = f"""No relevant documents found for this question. Please provide a brief general response:

{user_question}"""
        
        # Step 4: Get response from Ollama
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "model": settings.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_predict": 500,  # Reduce token limit for faster responses
                        "num_ctx": 2048     # Limit context window
                    }
                }
                
                print(f"Sending request to Ollama: {settings.ollama_url}/api/generate")
                print(f"Payload: {payload}")
                
                response = await client.post(
                    f"{settings.ollama_url}/api/generate",
                    json=payload,
                    timeout=60.0  # Reasonable 1-minute timeout
                )
                
                print(f"Ollama response status: {response.status_code}")
                print(f"Ollama response text: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get('response', 'Sorry, I could not generate a response.')
                else:
                    ai_response = f"AI service error: HTTP {response.status_code} - {response.text}"
                    
        except Exception as e:
            print(f"Exception in AI service: {e}")
            ai_response = f"Error communicating with AI service: {str(e)}"
        
        # Step 5: Let AI handle source relevance - return all sources if AI used context
        filtered_sources = []
        if context and all_sources and "no relevant" not in ai_response.lower():
            # Simple approach: if AI generated content from context, return all sources
            # Let the AI be responsible for only using relevant information
            for source_data in all_sources:
                filtered_sources.append(source_data['source'])
        
        return ai_response, filtered_sources
    
    def _extract_name_from_filename(self, filename: str) -> str:
        """Extract person name from filename like 'person3.pdf' -> 'Emily Rose Thompson'"""
        # This is a simple approach - could be enhanced with actual name mapping
        if 'person1' in filename:
            return "Sarah Michelle Johnson"
        elif 'person2' in filename:
            return "Marcus Antonio Rodriguez"  
        elif 'person3' in filename:
            return "Emily Rose Thompson"
        elif 'person4' in filename:
            return "Kevin Michael O'Brien"
        elif 'person5' in filename:
            return "Alexandra Sofia Petrov"
        return filename