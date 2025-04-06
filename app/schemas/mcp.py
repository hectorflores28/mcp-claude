from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union

class MCPRequest(BaseModel):
    """
    Solicitud MCP estándar
    """
    jsonrpc: str = Field("2.0", description="Versión de JSON-RPC")
    method: str = Field(..., description="Método a ejecutar")
    params: Dict[str, Any] = Field(..., description="Parámetros del método")
    id: Optional[str] = Field(None, description="Identificador de la solicitud")

class MCPResponse(BaseModel):
    """
    Respuesta MCP estándar
    """
    jsonrpc: str = Field("2.0", description="Versión de JSON-RPC")
    result: Optional[Any] = Field(None, description="Resultado de la operación")
    error: Optional[Dict[str, Any]] = Field(None, description="Información de error si ocurre")
    id: Optional[str] = Field(None, description="Identificador de la solicitud")

class MCPError(BaseModel):
    """
    Error MCP estándar
    """
    code: int = Field(..., description="Código de error")
    message: str = Field(..., description="Mensaje de error")
    data: Optional[Dict[str, Any]] = Field(None, description="Datos adicionales del error")

class ToolDefinition(BaseModel):
    """
    Definición de una herramienta MCP
    """
    name: str = Field(..., description="Nombre de la herramienta")
    description: str = Field(..., description="Descripción de la herramienta")
    parameters: Dict[str, Any] = Field(..., description="Esquema de parámetros de la herramienta")

class MCPToolsResponse(BaseModel):
    """
    Respuesta con lista de herramientas disponibles
    """
    tools: List[ToolDefinition] = Field(..., description="Lista de herramientas disponibles")

class MCPExecuteRequest(BaseModel):
    tool: str = Field(..., description="Nombre de la herramienta a ejecutar")
    parameters: Dict[str, Any] = Field(..., description="Parámetros de la herramienta")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")

class MCPExecuteResponse(BaseModel):
    result: Dict[str, Any]
    status: str
    message: Optional[str] = None

class MCPPromptTemplate(BaseModel):
    """
    Plantilla de prompt MCP
    """
    name: str = Field(..., description="Nombre de la plantilla")
    description: str = Field(..., description="Descripción de la plantilla")
    template: str = Field(..., description="Plantilla del prompt")
    variables: List[str] = Field(..., description="Variables requeridas en la plantilla")

class MCPPromptTemplatesResponse(BaseModel):
    templates: List[MCPPromptTemplate]

class MCPOperation(BaseModel):
    """
    Operación MCP
    """
    type: str = Field(..., description="Tipo de operación")
    tool: str = Field(..., description="Herramienta utilizada")
    parameters: Dict[str, Any] = Field(..., description="Parámetros de la operación")
    result: Optional[Any] = Field(None, description="Resultado de la operación")
    error: Optional[Dict[str, Any]] = Field(None, description="Error si ocurre")
    timestamp: str = Field(..., description="Marca de tiempo de la operación") 