from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import signal
import sys
from typing import Dict, Any
import time

from app.api.endpoints import router as api_router
from app.core.logging import LogManager
from app.core.config import settings
from app.services.mcp_service import MCPService

app = FastAPI(
    title="MCP-Claude API",
    description="API para integración con Claude Desktop usando el protocolo MCP",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
mcp_service = MCPService()

# Manejadores de señales para apagado graceful
def signal_handler(sig, frame):
    LogManager.log_info("Recibida señal de apagado, cerrando...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    LogManager.log_request(
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time
    )
    
    return response

# Middleware para manejo de errores
@app.middleware("http")
async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        LogManager.log_error("api", str(e))
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )

# Eventos de inicio y apagado
@app.on_event("startup")
async def startup_event():
    LogManager.log_info("Iniciando servidor MCP-Claude...")

@app.on_event("shutdown")
async def shutdown_event():
    LogManager.log_info("Cerrando servidor MCP-Claude...")

# Incluir routers
app.include_router(api_router, prefix="/api")

# Endpoints de salud y estado
@app.get("/health")
async def health_check():
    """
    Verifica el estado de salud del servidor
    """
    return {
        "status": "ok",
        "version": "0.1.0",
        "services": {
            "mcp": await mcp_service.get_status(),
            "logging": LogManager.is_available()
        }
    }

@app.get("/status")
async def status():
    """
    Obtiene el estado detallado del servidor
    """
    return {
        "status": "ok",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "services": {
            "mcp": await mcp_service.get_status(),
            "logging": LogManager.is_available()
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 