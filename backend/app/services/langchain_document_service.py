from typing import List, Optional
import os
from pathlib import Path

from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from typing import List
from langchain.schema import Document
from chromadb.config import Settings as ChromaSettings
import chromadb

from app.core.config import settings


class DefaultEmbeddings(Embeddings):
    """Simple wrapper for ChromaDB's default embedding function"""
    
    def __init__(self):
        # Use ChromaDB's default embedding function without creating a client
        import chromadb.utils.embedding_functions
        self._embedding_function = chromadb.utils.embedding_functions.DefaultEmbeddingFunction()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        return self._embedding_function(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        return self._embedding_function([text])[0]

class LangChainDocumentService:
    def __init__(self):
        # Use ChromaDB's default embeddings (simpler and more reliable)
        self.embeddings = DefaultEmbeddings()
        
        # Initialize text splitter with smart chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=[
                "\n\n",  # Double newlines (paragraphs)
                "\nCASE DETAILS:",
                "\nLEGAL ISSUES:",
                "\nDAMAGES:",
                "\nEMPLOYMENT DETAILS:",
                "\nPERSONAL INFORMATION:",
                "\nCLIENT ID:",
                "\n",  # Single newlines
                ". ",  # Sentences
                " ",   # Words
                ""     # Characters
            ]
        )
        
        # Initialize ChromaDB vector store with HTTP client
        import chromadb
        chroma_client = chromadb.HttpClient(
            host=settings.chroma_url.replace('http://', '').replace('https://', '').split(':')[0],
            port=int(settings.chroma_url.split(':')[-1])
        )
        
        self.vector_store = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=self.embeddings,
            client=chroma_client
        )
    
    async def process_document(self, file_path: str, filename: str) -> dict:
        """Process a document using LangChain loaders and splitters"""
        try:
            # Load document based on file type
            if filename.lower().endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif filename.lower().endswith('.txt'):
                loader = TextLoader(file_path, encoding='utf-8')
            else:
                raise ValueError(f"Unsupported file type: {filename}")
            
            # Load documents
            documents = loader.load()
            
            if not documents:
                raise ValueError(f"No content found in document: {filename}")
            
            # Add filename to metadata for all documents
            for doc in documents:
                doc.metadata["filename"] = filename
                # Ensure page number is set
                if "page" not in doc.metadata:
                    doc.metadata["page"] = 1
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            if not chunks:
                raise ValueError(f"No chunks created from document: {filename}")
            
            # Add to vector store
            self.vector_store.add_documents(chunks)
            
            return {
                "filename": filename,
                "pages": len(documents),
                "chunks": len(chunks),
                "message": f"Document processed successfully. {len(chunks)} chunks indexed."
            }
            
        except Exception as e:
            raise Exception(f"Error processing document {filename}: {str(e)}")
    
    async def delete_document(self, filename: str) -> dict:
        """Delete all chunks for a document from vector store"""
        try:
            # Get all document IDs for this filename
            results = self.vector_store.get(
                where={"filename": filename}
            )
            
            if results['ids']:
                # Delete the documents
                self.vector_store.delete(ids=results['ids'])
                return {
                    "message": f"Document {filename} deleted successfully. Removed {len(results['ids'])} chunks."
                }
            else:
                return {
                    "message": f"No chunks found for document {filename}"
                }
                
        except Exception as e:
            raise Exception(f"Error deleting document {filename}: {str(e)}")
    
    def get_retriever(self, **kwargs):
        """Get a retriever for the vector store"""
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": kwargs.get("k", 5),
                "score_threshold": kwargs.get("score_threshold", 0.3)
            }
        )
    
    async def similarity_search(self, query: str, k: int = 5, score_threshold: float = 0.3) -> List[Document]:
        """Perform similarity search"""
        try:
            # Use similarity search with score
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k
            )
            
            # Filter by score threshold (lower score = more similar)
            filtered_results = []
            for doc, score in results:
                # Convert ChromaDB distance to similarity (higher = more similar)
                similarity = 1 - (score / 2.0)
                if similarity >= score_threshold:
                    filtered_results.append(doc)
            
            print(f"Query: '{query}' - Found {len(results)} results, {len(filtered_results)} passed score threshold {score_threshold}")
            
            return filtered_results
            
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []
    
    async def get_all_documents(self) -> List[dict]:
        """Get metadata for all documents in the vector store"""
        try:
            # Get all documents
            results = self.vector_store.get()
            
            # Group by filename to get document info
            docs_info = {}
            for i, metadata in enumerate(results['metadatas']):
                filename = metadata.get('filename', 'unknown')
                if filename not in docs_info:
                    docs_info[filename] = {
                        'filename': filename,
                        'chunks': 0,
                        'pages': set()
                    }
                docs_info[filename]['chunks'] += 1
                if 'page' in metadata:
                    docs_info[filename]['pages'].add(metadata['page'])
            
            # Convert to list format
            document_list = []
            for filename, info in docs_info.items():
                document_list.append({
                    'filename': filename,
                    'chunks': info['chunks'],
                    'pages': len(info['pages']) if info['pages'] else 1,
                    'upload_date': None,  # ChromaDB doesn't store upload dates by default
                    'size_mb': 0.0  # Would need to calculate from content
                })
            
            return document_list
            
        except Exception as e:
            print(f"Error getting documents: {e}")
            return []