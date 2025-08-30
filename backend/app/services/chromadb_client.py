import chromadb
from app.core.config import settings

def get_chroma_client():
    """Get ChromaDB client with minimal configuration to avoid v1 API issues"""
    try:
        # Use the simplest possible configuration to avoid tenant validation
        client = chromadb.HttpClient(
            host=settings.chroma_url.replace('http://', '').split(':')[0],
            port=int(settings.chroma_url.split(':')[-1])
        )
        return client
    except Exception as e:
        print(f"ChromaDB connection error: {e}")
        # If even minimal config fails, we need to handle this gracefully
        raise Exception(f"Failed to connect to ChromaDB: {e}")