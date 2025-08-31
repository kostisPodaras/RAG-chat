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
                n_results=5  # Increase back to 5 for better coverage of multiple employees
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
            prompt = f"""Based on the following context from uploaded documents, please answer the user's question thoroughly. When looking for multiple items (like employees, records, etc.), make sure to check ALL sources and include ALL matches found in the context.

Context:
{context}

User Question: {user_question}

Instructions:
- Review ALL sources provided in the context
- Include ALL items that match the criteria from ANY source
- Reference which specific sources you used for each item
- Be thorough and don't miss any matching records

Answer:"""
        else:
            prompt = f"""No documents have been uploaded yet or no relevant information was found. Please provide a general response to this question:

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
                        "num_predict": 1000
                    }
                }
                
                print(f"Sending request to Ollama: {settings.ollama_url}/api/generate")
                print(f"Payload: {payload}")
                
                response = await client.post(
                    f"{settings.ollama_url}/api/generate",
                    json=payload,
                    timeout=120.0  # Increase timeout to 2 minutes for model loading
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
        
        # Step 5: Filter sources to only include ones mentioned in the AI response
        filtered_sources = []
        if context and all_sources:
            # Extract filenames mentioned in the AI response
            mentioned_files = set()
            for source_data in all_sources:
                filename = source_data['metadata']['filename']
                # Check if this filename or the person's name is mentioned in the AI response
                if filename.lower() in ai_response.lower() or self._extract_name_from_filename(filename).lower() in ai_response.lower():
                    mentioned_files.add(filename)
            
            # Only include sources that are actually mentioned in the response
            for source_data in all_sources:
                if source_data['metadata']['filename'] in mentioned_files:
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