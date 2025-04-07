from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class MCPVersion(str, Enum):
    """
    Versiones soportadas del protocolo MCP
    """
    V1_0 = "1.0"
    V1_1 = "1.1"

class MCPFeature(str, Enum):
    """
    Características soportadas del protocolo MCP
    """
    RESOURCES = "resources"
    TOOLS = "tools"
    FILESYSTEM = "filesystem"
    CACHE = "cache"
    LOGGING = "logging"
    PROMPTS = "prompts"

class MCPResourceType(str, Enum):
    """
    Tipos de recursos soportados
    """
    STATIC = "static"
    API = "api"
    CACHE = "cache"
    FILE = "file"
    DATABASE = "database"

class MCPAccessLevel(str, Enum):
    """
    Niveles de acceso soportados
    """
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

class MCPConfig(BaseModel):
    """
    Configuración del protocolo MCP
    """
    version: MCPVersion = Field(default=MCPVersion.V1_1, description="Versión del protocolo MCP")
    features: List[MCPFeature] = Field(default=[
        MCPFeature.RESOURCES,
        MCPFeature.TOOLS,
        MCPFeature.FILESYSTEM,
        MCPFeature.CACHE,
        MCPFeature.LOGGING,
        MCPFeature.PROMPTS
    ], description="Características soportadas")
    resource_types: List[MCPResourceType] = Field(default=[
        MCPResourceType.STATIC,
        MCPResourceType.API,
        MCPResourceType.CACHE,
        MCPResourceType.FILE,
        MCPResourceType.DATABASE
    ], description="Tipos de recursos soportados")
    access_levels: List[MCPAccessLevel] = Field(default=[
        MCPAccessLevel.READ,
        MCPAccessLevel.WRITE,
        MCPAccessLevel.EXECUTE,
        MCPAccessLevel.ADMIN
    ], description="Niveles de acceso soportados")
    max_request_size: int = Field(default=10485760, description="Tamaño máximo de solicitud en bytes")
    max_response_size: int = Field(default=10485760, description="Tamaño máximo de respuesta en bytes")
    timeout: int = Field(default=30, description="Tiempo de espera en segundos")
    rate_limit: int = Field(default=100, description="Límite de solicitudes por minuto")
    cache_ttl: int = Field(default=3600, description="Tiempo de vida de caché en segundos")
    log_level: str = Field(default="INFO", description="Nivel de logging")
    debug: bool = Field(default=False, description="Modo debug")

class MCPResourceConfig(BaseModel):
    """
    Configuración de recursos MCP
    """
    name: str = Field(..., description="Nombre del recurso")
    type: MCPResourceType = Field(..., description="Tipo de recurso")
    access: List[MCPAccessLevel] = Field(..., description="Niveles de acceso permitidos")
    parameters: Optional[Dict] = Field(default=None, description="Parámetros del recurso")
    cache_enabled: bool = Field(default=True, description="Si el recurso usa caché")
    cache_ttl: Optional[int] = Field(default=None, description="Tiempo de vida de caché específico")
    rate_limit: Optional[int] = Field(default=None, description="Límite de solicitudes específico")
    timeout: Optional[int] = Field(default=None, description="Tiempo de espera específico")

class MCPToolConfig(BaseModel):
    """
    Configuración de herramientas MCP
    """
    name: str = Field(..., description="Nombre de la herramienta")
    description: str = Field(..., description="Descripción de la herramienta")
    parameters: Dict = Field(..., description="Parámetros de la herramienta")
    required_resources: List[str] = Field(default=[], description="Recursos requeridos")
    cache_enabled: bool = Field(default=True, description="Si la herramienta usa caché")
    cache_ttl: Optional[int] = Field(default=None, description="Tiempo de vida de caché específico")
    rate_limit: Optional[int] = Field(default=None, description="Límite de solicitudes específico")
    timeout: Optional[int] = Field(default=None, description="Tiempo de espera específico")

# Configuración global del protocolo MCP
mcp_config = MCPConfig()

# Configuración de recursos predefinidos
mcp_resources = {
    "filesystem": MCPResourceConfig(
        name="filesystem",
        type=MCPResourceType.FILE,
        access=[MCPAccessLevel.READ, MCPAccessLevel.WRITE, MCPAccessLevel.EXECUTE],
        parameters={
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["create", "read", "update", "delete", "list"],
                    "description": "Operación a realizar"
                },
                "filename": {
                    "type": "string",
                    "description": "Nombre del archivo"
                },
                "content": {
                    "type": "string",
                    "description": "Contenido del archivo"
                }
            },
            "required": ["operation"]
        }
    ),
    "claude": MCPResourceConfig(
        name="claude",
        type=MCPResourceType.API,
        access=[MCPAccessLevel.EXECUTE],
        parameters={
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["completion", "analyze", "generate"],
                    "description": "Operación a realizar"
                },
                "text": {
                    "type": "string",
                    "description": "Texto a procesar"
                },
                "max_tokens": {
                    "type": "integer",
                    "description": "Número máximo de tokens",
                    "default": 4096
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperatura para la generación",
                    "default": 0.7
                }
            },
            "required": ["operation", "text"]
        }
    ),
    "search": MCPResourceConfig(
        name="search",
        type=MCPResourceType.API,
        access=[MCPAccessLevel.READ],
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Término de búsqueda"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Número de resultados",
                    "default": 5
                },
                "analyze": {
                    "type": "boolean",
                    "description": "Si se debe analizar los resultados",
                    "default": False
                }
            },
            "required": ["query"]
        }
    ),
    "cache": MCPResourceConfig(
        name="cache",
        type=MCPResourceType.CACHE,
        access=[MCPAccessLevel.READ, MCPAccessLevel.WRITE],
        parameters={
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "Clave de caché"
                },
                "value": {
                    "type": "any",
                    "description": "Valor a almacenar"
                },
                "ttl": {
                    "type": "integer",
                    "description": "Tiempo de vida en segundos",
                    "default": 3600
                }
            },
            "required": ["key"]
        }
    )
}

# Configuración de herramientas predefinidas
mcp_tools = {
    "buscar_en_brave": MCPToolConfig(
        name="buscar_en_brave",
        description="Busca información en la web usando Brave Search",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Término de búsqueda"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Número de resultados",
                    "default": 5
                },
                "analyze": {
                    "type": "boolean",
                    "description": "Si se debe analizar los resultados",
                    "default": False
                }
            },
            "required": ["query"]
        },
        required_resources=["search"]
    ),
    "generar_markdown": MCPToolConfig(
        name="generar_markdown",
        description="Genera contenido en formato Markdown",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Contenido a formatear"
                },
                "format_type": {
                    "type": "string",
                    "enum": ["article", "document", "code"],
                    "description": "Tipo de formato",
                    "default": "article"
                }
            },
            "required": ["content"]
        },
        required_resources=["claude"]
    ),
    "analizar_texto": MCPToolConfig(
        name="analizar_texto",
        description="Analiza texto usando Claude",
        parameters={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Texto a analizar"
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["summary", "sentiment", "keywords", "entities"],
                    "description": "Tipo de análisis",
                    "default": "summary"
                }
            },
            "required": ["text"]
        },
        required_resources=["claude"]
    )
} 