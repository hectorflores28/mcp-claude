from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import search, filesystem, tools
from app.core.config import settings
from app.core.logging import LogManager

app = FastAPI(
    title="MCP-Claude Server",
    description="Servidor MCP personalizado con Claude, Brave Search y sistema de archivos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(tools.router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(filesystem.router, prefix="/api/v1/filesystem", tags=["filesystem"])

@app.on_event("startup")
async def startup_event():
    """
    Inicialización al arrancar la aplicación
    """
    LogManager.log_info("Iniciando servidor MCP-Claude")
    # Crear directorios necesarios
    for directory in [settings.LOG_DIR, settings.DATA_DIR, settings.TEMP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Limpieza al cerrar la aplicación
    """
    LogManager.log_info("Cerrando servidor MCP-Claude")

@app.get("/")
async def root():
    """
    Endpoint de salud
    """
    return {
        "status": "ok",
        "service": "MCP-Claude Server",
        "version": "1.0.0"
    } 