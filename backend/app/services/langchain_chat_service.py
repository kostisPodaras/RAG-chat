from typing import List, Tuple
import asyncio

from langchain.llms.base import LLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.callbacks.manager import CallbackManagerForLLMRun
import httpx

from app.core.config import settings
from app.models.schemas import SourceReference
from app.services.langchain_document_service import LangChainDocumentService

class OllamaLLM(LLM):
    """Custom Ollama LLM for LangChain"""
    
    @property
    def _llm_type(self) -> str:
        return "ollama"
    
    def _call(
        self,
        prompt: str,
        stop: List[str] = None,
        run_manager: CallbackManagerForLLMRun = None,
        **kwargs,
    ) -> str:
        """Call Ollama API synchronously"""
        return asyncio.run(self._acall(prompt, stop, run_manager, **kwargs))
    
    async def _acall(
        self,
        prompt: str,
        stop: List[str] = None,
        run_manager: CallbackManagerForLLMRun = None,
        **kwargs,
    ) -> str:
        """Call Ollama API asynchronously"""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "model": settings.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", 0.7),
                        "top_p": kwargs.get("top_p", 0.9),
                        "num_predict": kwargs.get("num_predict", 500),
                        "num_ctx": kwargs.get("num_ctx", 2048)
                    }
                }
                
                response = await client.post(
                    f"{settings.ollama_url}/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('response', 'Sorry, I could not generate a response.')
                else:
                    return f"AI service error: HTTP {response.status_code}"
                    
        except Exception as e:
            return f"Error communicating with AI service: {str(e)}"

class LangChainChatService:
    def __init__(self):
        # Initialize document service
        self.document_service = LangChainDocumentService()
        
        # Initialize LLM
        self.llm = OllamaLLM()
        
        # Create prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""Answer the question based on the provided context. Be direct and concise.

Context:
{context}

Question: {question}

Answer:"""
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.document_service.get_retriever(k=5, score_threshold=0.3),
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": self.prompt_template
            }
        )
    
    async def get_response(self, user_question: str) -> Tuple[str, List[SourceReference]]:
        """Get AI response using LangChain RAG pipeline"""
        try:
            # Run the QA chain
            result = await asyncio.to_thread(
                self.qa_chain,
                {"query": user_question}
            )
            
            # Extract response and source documents
            ai_response = result["result"]
            source_documents = result.get("source_documents", [])
            
            # Convert source documents to SourceReference objects
            sources = []
            for doc in source_documents:
                metadata = doc.metadata
                sources.append(SourceReference(
                    filename=metadata.get("filename", "unknown"),
                    page=metadata.get("page", 1),
                    content=doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                ))
            
            print(f"LangChain QA Chain - Query: '{user_question}' - Retrieved {len(source_documents)} sources")
            
            return ai_response, sources
            
        except Exception as e:
            print(f"Error in LangChain chat service: {e}")
            return f"Error processing your question: {str(e)}", []
    
    async def get_response_with_custom_retrieval(self, user_question: str, k: int = 5, score_threshold: float = 0.3) -> Tuple[str, List[SourceReference]]:
        """Get response with custom retrieval parameters"""
        try:
            # Perform custom similarity search
            relevant_docs = await self.document_service.similarity_search(
                query=user_question,
                k=k,
                score_threshold=score_threshold
            )
            
            if not relevant_docs:
                return "No relevant information found in the documents.", []
            
            # Prepare context from retrieved documents
            context = "\n\n".join([
                f"Source {i+1} (from {doc.metadata.get('filename', 'unknown')}, page {doc.metadata.get('page', 1)}):\n{doc.page_content}"
                for i, doc in enumerate(relevant_docs)
            ])
            
            # Generate response using LLM
            prompt = self.prompt_template.format(
                context=context,
                question=user_question
            )
            
            ai_response = await self.llm._acall(prompt)
            
            # Convert to source references
            sources = []
            for doc in relevant_docs:
                metadata = doc.metadata
                sources.append(SourceReference(
                    filename=metadata.get("filename", "unknown"),
                    page=metadata.get("page", 1),
                    content=doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                ))
            
            print(f"Custom Retrieval - Query: '{user_question}' - Retrieved {len(relevant_docs)} sources")
            
            return ai_response, sources
            
        except Exception as e:
            print(f"Error in custom retrieval: {e}")
            return f"Error processing your question: {str(e)}", []