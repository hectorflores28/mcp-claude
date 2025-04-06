from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union

class MCPRequest(BaseModel):
    """
    Solicitud genérica para herramientas MCP
    """
    jsonrpc: str = "2.0"
    method: str = Field(..., description="Método a ejecutar")
    params: Dict[str, Any] = Field(..., description="Parámetros del método")
    id: Optional[str] = None

class MCPResponse(BaseModel):
    """
    Respuesta genérica de herramientas MCP
    """
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class MCPError(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

class ToolDefinition(BaseModel):
    """
    Definición de una herramienta MCP
    """
    name: str
    description: str
    parameters: Dict[str, Any]

class MCPToolsResponse(BaseModel):
    """
    Respuesta del endpoint de herramientas
    """
    tools: List[ToolDefinition]

class MCPExecuteRequest(BaseModel):
    tool: str = Field(..., description="Nombre de la herramienta a ejecutar")
    parameters: Dict[str, Any] = Field(..., description="Parámetros de la herramienta")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")

class MCPExecuteResponse(BaseModel):
    result: Dict[str, Any]
    status: str
    message: Optional[str] = None

class MCPPromptTemplate(BaseModel):
    name: str
    description: str
    template: str
    parameters: List[str]

class MCPPromptTemplatesResponse(BaseModel):
    templates: List[MCPPromptTemplate] 