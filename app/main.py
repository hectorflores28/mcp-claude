from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints import (
    search,
    filesystem,
    tools,
    mcp,
    claude,
    prompts,
    logs,
    health
)
from app.core.config import settings
from app.core.logging import LogManager
import uvicorn

app = FastAPI(
    title="MCP Claude API",
    description="API para integración con Claude y herramientas MCP",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(search.router, prefix="/api")
app.include_router(filesystem.router, prefix="/api")
app.include_router(tools.router, prefix="/api")
app.include_router(mcp.router, prefix="/api")
app.include_router(claude.router, prefix="/api")
app.include_router(prompts.router, prefix="/api")
app.include_router(logs.router, prefix="/api")
app.include_router(health.router, prefix="/api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para registrar todas las solicitudes HTTP
    """
    # Registrar solicitud
    LogManager.log_api_request(
        method=request.method,
        path=request.url.path,
        data=await request.json() if request.method in ["POST", "PUT"] else None
    )
    
    # Procesar solicitud
    response = await call_next(request)
    
    # Registrar respuesta
    LogManager.log_api_response(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code
    )
    
    return response

@app.on_event("startup")
async def startup_event():
    """
    Evento de inicio de la aplicación
    """
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

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    ) 