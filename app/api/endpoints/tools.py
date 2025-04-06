from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.schemas.mcp import MCPToolsResponse, ToolDefinition, MCPRequest, MCPResponse
from app.schemas.search import SearchToolSchema
from app.schemas.filesystem import FileSystemToolSchema
from app.core.logging import LogManager
from app.core.search import BraveSearch
from app.core.filesystem import FileSystem
from app.core.claude import ClaudeClient

router = APIRouter()

@router.get("/", response_model=MCPToolsResponse)
async def list_tools():
    """
    Lista todas las herramientas MCP disponibles.
    
    Returns:
        Lista de herramientas con sus esquemas
    """
    try:
        # Registrar la solicitud
        LogManager.log_api_request("GET", "/api/v1/tools")
        
        # Definir las herramientas disponibles
        tools = [
            ToolDefinition(
                name="buscar_en_brave",
                description="Realiza búsquedas web usando Brave Search API",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Término de búsqueda"},
                        "num_results": {"type": "number", "description": "Número de resultados a devolver"},
                        "analyze": {"type": "boolean", "description": "Si se debe analizar los resultados con Claude"}
                    },
                    "required": ["query"]
                }
            ),
            ToolDefinition(
                name="filesystem",
                description="Operaciones CRUD en el sistema de archivos",
                parameters={
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string", 
                            "description": "Operación a realizar (create, read, list, delete)",
                            "enum": ["create", "read", "list", "delete"]
                        },
                        "filename": {"type": "string", "description": "Nombre del archivo"},
                        "content": {"type": "string", "description": "Contenido del archivo (para create)"}
                    },
                    "required": ["operation"]
                }
            ),
            ToolDefinition(
                name="generar_markdown",
                description="Genera contenido en formato Markdown usando Claude",
                parameters={
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Contenido a formatear"},
                        "format_type": {"type": "string", "description": "Tipo de formato (article, documentation, etc.)"},
                        "save": {"type": "boolean", "description": "Si se debe guardar el archivo"},
                        "filename": {"type": "string", "description": "Nombre del archivo a guardar"}
                    },
                    "required": ["content"]
                }
            ),
            ToolDefinition(
                name="analizar_texto",
                description="Analiza un texto usando Claude",
                parameters={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Texto a analizar"},
                        "analysis_type": {
                            "type": "string", 
                            "description": "Tipo de análisis (summary, concepts, sentiment)",
                            "enum": ["summary", "concepts", "sentiment"]
                        }
                    },
                    "required": ["text", "analysis_type"]
                }
            )
        ]
        
        return MCPToolsResponse(tools=tools)
    
    except Exception as e:
        # Registrar el error
        LogManager.log_error("list_tools", str(e))
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