from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    
    # Database
    database_url: str = "sqlite:///./data/chat_history.db"
    
    # Ollama Configuration
    ollama_url: str = "http://ollama:11434"
    ollama_model: str = "llama3.1:8b"
    
    # ChromaDB Configuration
    chroma_url: str = "http://chromadb:8000"
    chroma_collection_name: str = "documents"
    
    # File Upload Configuration
    max_file_size_mb: int = 50
    allowed_extensions: List[str] = ["pdf", "txt"]
    upload_dir: str = "uploads"
    
    # Privacy & Security
    telemetry_disabled: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()