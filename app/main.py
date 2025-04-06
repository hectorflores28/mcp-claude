from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints import search, filesystem, tools
from app.core.config import settings
from app.core.logging import LogManager
import uvicorn

app = FastAPI(
    title="MCP-Claude API",
    description="API para el servidor MCP personalizado con Claude, Brave Search y sistema de archivos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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

# Endpoint principal para ejecución de herramientas MCP
@app.post("/mcp/execute")
async def execute_mcp(request: dict):
    """
    Endpoint principal para ejecutar herramientas MCP según el protocolo JSON-RPC 2.0.
    
    Args:
        request: Solicitud JSON-RPC 2.0
        
    Returns:
        Respuesta JSON-RPC 2.0
    """
    try:
        # Registrar la solicitud
        LogManager.log_operation("mcp", "execute", request)
        
        # Redirigir a la función de ejecución de herramientas
        from app.api.endpoints.tools import execute_tool
        from app.schemas.mcp import MCPRequest
        
        # Convertir dict a MCPRequest
        mcp_request = MCPRequest(**request)
        
        # Ejecutar herramienta
        response = await execute_tool(mcp_request)
        
        return response
        
    except Exception as e:
        LogManager.log_error("mcp", str(e))
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": f"Error al ejecutar solicitud MCP: {str(e)}"
                },
                "id": request.get("id", None)
            }
        )

@app.get("/")
async def root():
    """
    Endpoint raíz que proporciona información básica sobre la API.
    """
    return {
        "name": "MCP-Claude API",
        "version": "1.0.0",
        "description": "API para el servidor MCP personalizado con Claude, Brave Search y sistema de archivos",
        "documentation": "/docs"
    }

@app.on_event("startup")
async def startup_event():
    """
    Evento de inicio de la aplicación.
    """
    LogManager.log_info("API iniciada")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento de cierre de la aplicación.
    """
    LogManager.log_info("API detenida")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 