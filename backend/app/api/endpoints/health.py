from fastapi import APIRouter, HTTPException
from datetime import datetime
import httpx
import asyncio

from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of all services"""
    services = {}
    
    # Check Ollama
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.ollama_url}/api/tags", timeout=5.0)
            services["ollama"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        services["ollama"] = "unhealthy"
    
    # Check ChromaDB (using heartbeat endpoint)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.chroma_url}/api/v1/heartbeat", timeout=5.0)
            services["chromadb"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        services["chromadb"] = "unhealthy"
    
    # Check if critical services are healthy
    critical_services = ["ollama", "chromadb"]
    all_healthy = all(services.get(service) == "healthy" for service in critical_services)
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        services=services,
        timestamp=datetime.utcnow()
    )