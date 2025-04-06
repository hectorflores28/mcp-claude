from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel
from app.services.brave_search import BraveSearchService
from app.services.claude_service import ClaudeService
from app.services.filesystem_service import FileSystemService

router = APIRouter()
brave_search = BraveSearchService()
claude = ClaudeService()
filesystem = FileSystemService()

class MCPRequest(BaseModel):
    tool: str
    parameters: Dict
    context: Optional[Dict] = None

class MCPResponse(BaseModel):
    result: Dict
    status: str
    message: Optional[str] = None

@router.post("/execute", response_model=MCPResponse)
async def execute_mcp(request: MCPRequest):
    """
    Ejecuta una herramienta MCP.
    
    Args:
        request: Solicitud MCP con herramienta y parámetros
        
    Returns:
        Resultado de la ejecución
    """
    try:
        if request.tool == "buscar_en_brave":
            results = await brave_search.get_web_results(
                query=request.parameters.get("query", ""),
                num_results=request.parameters.get("num_results", 10)
            )
            
            # Si se solicita análisis de resultados
            if request.parameters.get("analyze", False):
                analysis = await claude.analyze_search_results(
                    query=request.parameters["query"],
                    results=results
                )
                return MCPResponse(
                    result={
                        "search_results": results,
                        "analysis": analysis
                    },
                    status="success"
                )
            
            return MCPResponse(
                result={"search_results": results},
                status="success"
            )
            
        elif request.tool == "generar_markdown":
            content = request.parameters.get("content", "")
            format_type = request.parameters.get("format_type", "article")
            
            markdown = await claude.generate_markdown(content, format_type)
            
            # Si se solicita guardar el archivo
            if request.parameters.get("save", False):
                filename = request.parameters.get("filename", "output.md")
                await filesystem.save_file(markdown, filename)
                return MCPResponse(
                    result={
                        "content": markdown,
                        "saved_as": filename
                    },
                    status="success"
                )
            
            return MCPResponse(
                result={"content": markdown},
                status="success"
            )
            
        elif request.tool == "listar_archivos":
            files = await filesystem.list_files()
            return MCPResponse(
                result={"files": files},
                status="success"
            )
            
        elif request.tool == "leer_archivo":
            filename = request.parameters.get("filename")
            if not filename:
                raise ValueError("Se requiere el nombre del archivo")
                
            content = await filesystem.read_file(filename)
            return MCPResponse(
                result=content,
                status="success"
            )
            
        else:
            raise ValueError(f"Herramienta no soportada: {request.tool}")
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al ejecutar la herramienta: {str(e)}"
        ) 