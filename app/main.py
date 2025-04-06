from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import search, filesystem, mcp

app = FastAPI(
    title="MCP-Claude",
    description="Servidor MCP personalizado con Claude y Brave Search",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(filesystem.router, prefix="/api/v1/filesystem", tags=["filesystem"])
app.include_router(mcp.router, prefix="/api/v1/mcp", tags=["mcp"])

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a MCP-Claude",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 