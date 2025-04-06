from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.schemas.mcp import MCPToolsResponse, ToolDefinition, MCPRequest, MCPResponse
from app.schemas.search import SearchToolSchema
from app.schemas.filesystem import FileSystemToolSchema
from app.core.logging import LogManager
from app.core.search import BraveSearch
from app.core.filesystem import FileSystem
from app.core.claude import ClaudeClient
from app.core.security import verify_api_key

router = APIRouter(prefix="/tools", tags=["tools"])

# Definición de herramientas disponibles
AVAILABLE_TOOLS = [
    ToolDefinition(
        name="buscar_en_brave",
        description="Realiza una búsqueda web utilizando Brave Search API",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Término de búsqueda"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Número de resultados a retornar",
                    "default": 5
                },
                "country": {
                    "type": "string",
                    "description": "Código de país para resultados",
                    "default": "es"
                },
                "language": {
                    "type": "string",
                    "description": "Idioma de los resultados",
                    "default": "es"
                },
                "analyze": {
                    "type": "boolean",
                    "description": "Si se debe analizar los resultados con Claude",
                    "default": False
                }
            },
            "required": ["query"]
        }
    ),
    ToolDefinition(
        name="gestionar_archivo",
        description="Realiza operaciones CRUD en archivos Markdown",
        parameters={
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "Tipo de operación (create, read, update, delete)",
                    "enum": ["create", "read", "update", "delete"]
                },
                "filename": {
                    "type": "string",
                    "description": "Nombre del archivo"
                },
                "content": {
                    "type": "string",
                    "description": "Contenido del archivo (para create/update)"
                }
            },
            "required": ["operation", "filename"]
        }
    )
]

@router.get("/", response_model=MCPToolsResponse)
async def list_tools(
    api_key: str = Depends(verify_api_key)
):
    """
    Lista todas las herramientas MCP disponibles.
    
    Args:
        api_key: API key para autenticación
        
    Returns:
        MCPToolsResponse: Lista de herramientas disponibles
    """
    try:
        # Registrar operación
        LogManager.log_operation(
            "tools",
            "list_tools",
            {"count": len(AVAILABLE_TOOLS)}
        )
        
        return MCPToolsResponse(tools=AVAILABLE_TOOLS)
        
    except Exception as e:
        LogManager.log_error("tools", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar herramientas: {str(e)}"
        )

@router.post("/execute", response_model=MCPResponse)
async def execute_tool(request: MCPRequest):
    """
    Ejecuta una herramienta MCP específica.
    
    Args:
        request: Solicitud con la herramienta y parámetros a ejecutar
        
    Returns:
        Resultado de la ejecución de la herramienta
    """
    try:
        # Registrar la solicitud
        LogManager.log_api_request("POST", "/api/v1/tools/execute", request.dict())
        
        # Ejecutar la herramienta correspondiente
        if request.tool == "buscar_en_brave":
            search = BraveSearch()
            result = await search.search(
                query=request.parameters["query"],
                num_results=request.parameters.get("num_results", 5),
                analyze=request.parameters.get("analyze", False)
            )
            
        elif request.tool == "filesystem":
            fs = FileSystem()
            operation = request.parameters["operation"]
            
            if operation == "create":
                result = await fs.create_file(
                    filename=request.parameters["filename"],
                    content=request.parameters["content"]
                )
            elif operation == "read":
                result = await fs.read_file(request.parameters["filename"])
            elif operation == "list":
                result = await fs.list_files()
            elif operation == "delete":
                result = await fs.delete_file(request.parameters["filename"])
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Operación no válida: {operation}"
                )
                
        elif request.tool == "generar_markdown":
            claude = ClaudeClient()
            result = await claude.generate_markdown(
                content=request.parameters["content"],
                format_type=request.parameters.get("format_type", "article"),
                save=request.parameters.get("save", False),
                filename=request.parameters.get("filename")
            )
            
        elif request.tool == "analizar_texto":
            claude = ClaudeClient()
            result = await claude.analyze_text(
                text=request.parameters["text"],
                analysis_type=request.parameters["analysis_type"]
            )
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Herramienta no válida: {request.tool}"
            )
            
        return MCPResponse(result=result)
        
    except Exception as e:
        # Registrar el error
        LogManager.log_error("execute_tool", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al ejecutar herramienta: {str(e)}"
        ) 