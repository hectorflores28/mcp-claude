from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.api.endpoints import (
    # search_router,
    filesystem_router,
    tools_router,
    health_router,
    claude_router,
    prompts_router,
    logs_router
)
from app.core.config import settings
from app.core.logging import LogManager
from app.core.exceptions import MCPClaudeError
from app.core.error_handlers import mcp_claude_error_handler, http_exception_handler
import uvicorn

app = FastAPI(
    title="MCP Claude API",
    description="API para integración con Claude y herramientas MCP",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporalmente permite todos los orígenes para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar manejadores de errores
app.add_exception_handler(MCPClaudeError, mcp_claude_error_handler)
app.add_exception_handler(Exception, http_exception_handler)

# Incluir routers
# app.include_router(search_router, prefix="/api", tags=["search"])
app.include_router(filesystem_router, prefix="/api", tags=["filesystem"])
app.include_router(tools_router, prefix="/api", tags=["tools"])
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(claude_router, prefix="/api", tags=["claude"])
app.include_router(prompts_router, prefix="/api", tags=["prompts"])
app.include_router(logs_router, prefix="/api", tags=["logs"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para registrar todas las solicitudes HTTP
    """
    start_time = time.time()
    
    # Registrar solicitud
    data = None
    if request.method in ["POST", "PUT"]:
        try:
            data = await request.json()
        except:
            data = None
            
    LogManager.log_api_request(
        method=request.method,
        path=request.url.path,
        data=data
    )
    
    # Procesar solicitud
    response = await call_next(request)
    
    # Calcular tiempo de respuesta
    response_time = time.time() - start_time
    
    # Registrar respuesta
    LogManager.log_api_response(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        response_time=response_time
    )
    
    return response

@app.on_event("startup")
async def startup_event():
    """
    Evento de inicio de la aplicación
    """
    LogManager.setup_logger()
    LogManager.log_info("Iniciando MCP Claude API...")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento de cierre de la aplicación
    """
    LogManager.log_info("Cerrando MCP Claude API...")

@app.get("/")
async def root():
    """
    Endpoint raíz
    """
    return {
        "name": "MCP Claude API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """
    Endpoint de salud detallado
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "services": {
            "claude": "available",
            "filesystem": "available",
            "logging": "available"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    ) 