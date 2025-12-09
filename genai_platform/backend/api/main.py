"""
GenAI Platform - FastAPI Server
REST API endpoints for querying, ingestion, and administration
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from loguru import logger
import sys

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO")

# Create FastAPI app
app = FastAPI(
    title="GenAI Platform API",
    description="Enterprise AI Orchestration Platform REST API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request/Response Models

class QueryRequest(BaseModel):
    """User query request"""
    prompt: str
    division_id: str
    department_id: str
    persona_id: Optional[str] = None
    model_id: Optional[str] = None


class QueryResponse(BaseModel):
    """Query response"""
    text: str
    model_id: str
    provider: str
    tokens_used: int
    cost: float
    redacted_pii: List[str] = []


class ConfigResponse(BaseModel):
    """Configuration response"""
    divisions: List[Dict[str, Any]]
    models: List[Dict[str, Any]]
    personas: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    components: Dict[str, bool]


# ============================================================
# Health & Status Endpoints

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check system health"""
    try:
        from backend.config_manager import get_config
        from backend.models.model_router import ModelRouter
        
        conf = get_config()
        router = ModelRouter()
        
        return {
            "status": "operational",
            "version": "1.0.0",
            "components": {
                "configuration": True,
                "models": len(router.get_available_models()) > 0,
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="System health check failed")


@app.get("/api/version")
async def version():
    """Get version information"""
    return {
        "version": "1.0.0",
        "name": "GenAI Platform",
        "description": "Enterprise AI Orchestration System"
    }


@app.get("/api/config", response_model=ConfigResponse)
async def get_config_endpoint():
    """Get current configuration"""
    try:
        from backend.config_manager import get_config
        conf = get_config()
        
        return {
            "divisions": conf.list_divisions(),
            "models": conf.list_models(),
            "personas": conf.list_personas(),
        }
    except Exception as e:
        logger.error(f"Config retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve configuration")


# ============================================================
# Query Endpoints

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process user query
    
    Submits a query with context (division, department, persona, model) and returns
    AI-generated response with cost tracking and PII redaction.
    """
    try:
        from backend.orchestration.query_processor import QueryProcessor, QueryContext
        
        processor = QueryProcessor()
        context = QueryContext(
            user_id="api_user",  # In production, extract from auth token
            division_id=request.division_id,
            department_id=request.department_id,
            persona_id=request.persona_id or "general_assistant",
            model_id=request.model_id,
            role_id="analyst"  # In production, extract from auth token
        )
        
        response = processor.process(request.prompt, context)
        
        return {
            "text": response.text,
            "model_id": response.model_id,
            "provider": response.provider,
            "tokens_used": response.tokens_used,
            "cost": response.cost,
            "redacted_pii": [str(p) for p in response.redacted_pii],
        }
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


# ============================================================
# Division Endpoints

@app.get("/api/divisions")
async def list_divisions():
    """List all divisions"""
    try:
        from backend.config_manager import get_config
        conf = get_config()
        return conf.list_divisions()
    except Exception as e:
        logger.error(f"Division retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve divisions")


@app.get("/api/divisions/{division_id}")
async def get_division(division_id: str):
    """Get division by ID"""
    try:
        from backend.config_manager import get_config
        conf = get_config()
        division = conf.get_division(division_id)
        
        if not division:
            raise HTTPException(status_code=404, detail=f"Division not found: {division_id}")
        
        return division
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Division retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve division")


# ============================================================
# Model Endpoints

@app.get("/api/models")
async def list_models():
    """List all available models"""
    try:
        from backend.config_manager import get_config
        conf = get_config()
        return conf.list_models()
    except Exception as e:
        logger.error(f"Model retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve models")


@app.get("/api/models/{model_id}")
async def get_model(model_id: str):
    """Get model configuration by ID"""
    try:
        from backend.config_manager import get_config
        conf = get_config()
        model = conf.get_model(model_id)
        
        if not model:
            raise HTTPException(status_code=404, detail=f"Model not found: {model_id}")
        
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Model retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model")


# ============================================================
# Persona Endpoints

@app.get("/api/personas")
async def list_personas():
    """List all available personas"""
    try:
        from backend.config_manager import get_config
        conf = get_config()
        return conf.list_personas()
    except Exception as e:
        logger.error(f"Persona retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve personas")


# ============================================================
# Root Endpoint

@app.get("/")
async def root():
    """Root endpoint - API documentation"""
    return {
        "name": "GenAI Platform API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health",
        "endpoints": {
            "health": "GET /api/health",
            "config": "GET /api/config",
            "query": "POST /api/query",
            "divisions": "GET /api/divisions",
            "models": "GET /api/models",
            "personas": "GET /api/personas",
        }
    }


def main():
    """Main entry point for API server"""
    import uvicorn
    
    logger.info("Starting GenAI Platform API server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
