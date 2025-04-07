from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
import time
from app.core.config import settings
from app.core.logging import LogManager
from app.core.mcp_config import (
    mcp_config,
    mcp_resources,
    mcp_tools,
    MCPVersion,
    MCPFeature,
    MCPResourceType,
    MCPAccessLevel,
    MCPResourceConfig,
    MCPToolConfig
)
from app.services.resources_service import ResourcesService
from app.services.filesystem_service import FileSystemService
from app.services.claude_service import ClaudeService
from app.services.cache import CacheService
from app.schemas.mcp import MCPStatus, MCPOperation

class MCPService:
    """
    Servicio para gestionar el protocolo MCP
    """
    def __init__(self):
        self.resources_service = ResourcesService()
        self.filesystem_service = FileSystemService()
        self.claude_service = ClaudeService()
        self.cache_service = CacheService()
        self.config = mcp_config
        self.resources = mcp_resources
        self.tools = mcp_tools
        self.operations: List[MCPOperation] = []
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado del protocolo MCP
        
        Returns:
            Dict con el estado del protocolo
        """
        status = MCPStatus(
            version=self.config.version.value,
            features=[feature.value for feature in self.config.features],
            resource_types=[rtype.value for rtype in self.config.resource_types],
            access_levels=[level.value for level in self.config.access_levels],
            resources=list(self.resources.keys()),
            tools=list(self.tools.keys())
        )
        return status.dict()
    
    async def validate_request(self, request: Dict[str, Any]) -> bool:
        """
        Valida una solicitud MCP
        
        Args:
            request: Solicitud a validar
            
        Returns:
            True si la solicitud es válida, False en caso contrario
        """
        try:
            # Verificar versión
            if "version" not in request:
                return False
            
            # Verificar método
            if "method" not in request:
                return False
            
            # Verificar parámetros
            if "params" not in request:
                return False
            
            # Verificar tamaño
            request_size = len(json.dumps(request).encode())
            if request_size > self.config.max_request_size:
                return False
            
            # Verificar rate limit
            if not await self._check_rate_limit(request):
                return False
            
            return True
            
        except Exception as e:
            LogManager.log_error("mcp", f"Error al validar solicitud: {str(e)}")
            return False
    
    async def _check_rate_limit(self, request: Dict[str, Any]) -> bool:
        """
        Verifica el rate limit de una solicitud
        
        Args:
            request: Solicitud a verificar
            
        Returns:
            True si está dentro del límite, False en caso contrario
        """
        try:
            # Obtener límite del recurso o herramienta
            method = request["method"]
            params = request["params"]
            
            if method == "execute_tool":
                tool_name = params.get("name")
                tool = self.tools.get(tool_name)
                if tool and tool.rate_limit:
                    limit = tool.rate_limit
                else:
                    limit = self.config.rate_limit
            else:
                limit = self.config.rate_limit
            
            # Verificar en caché
            key = f"rate_limit:{method}:{datetime.now().strftime('%Y%m%d%H%M')}"
            count = await self.cache_service.get(key) or 0
            
            if count >= limit:
                return False
            
            # Incrementar contador
            await self.cache_service.set(key, count + 1, ttl=60)
            return True
            
        except Exception as e:
            LogManager.log_error("mcp", f"Error al verificar rate limit: {str(e)}")
            return True
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una solicitud MCP
        
        Args:
            request: Solicitud a procesar
            
        Returns:
            Dict con la respuesta
        """
        start_time = time.time()
        operation = None
        
        try:
            # Validar solicitud
            if not await self.validate_request(request):
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 400,
                        "message": "Solicitud inválida"
                    },
                    "id": request.get("id"),
                    "version": request.get("version", "1.1")
                }
            
            # Procesar según el método
            method = request["method"]
            params = request["params"]
            
            # Crear operación
            operation = MCPOperation(
                type="request",
                tool=method,
                parameters=params,
                timestamp=datetime.now().isoformat(),
                version=request.get("version", "1.1")
            )
            
            if method == "list_resources":
                response = await self.resources_service.list_resources()
            elif method == "get_resource":
                response = await self.resources_service.get_resource(params["name"])
            elif method == "access_resource":
                response = await self.resources_service.access_resource(params)
            elif method == "list_tools":
                response = {
                    "jsonrpc": "2.0",
                    "result": list(self.tools.keys()),
                    "id": request.get("id"),
                    "version": request.get("version", "1.1")
                }
            elif method == "get_tool":
                tool = self.tools.get(params["name"])
                if tool:
                    response = {
                        "jsonrpc": "2.0",
                        "result": tool.dict(),
                        "id": request.get("id"),
                        "version": request.get("version", "1.1")
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": 404,
                            "message": f"Herramienta no encontrada: {params['name']}"
                        },
                        "id": request.get("id"),
                        "version": request.get("version", "1.1")
                    }
            elif method == "execute_tool":
                response = await self._execute_tool(params)
            else:
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 404,
                        "message": f"Método no encontrado: {method}"
                    },
                    "id": request.get("id"),
                    "version": request.get("version", "1.1")
                }
            
            # Verificar tamaño de respuesta
            response_size = len(json.dumps(response).encode())
            if response_size > self.config.max_response_size:
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 500,
                        "message": "Respuesta demasiado grande"
                    },
                    "id": request.get("id"),
                    "version": request.get("version", "1.1")
                }
            
            # Actualizar operación
            if operation:
                operation.result = response.get("result")
                operation.error = response.get("error")
                operation.execution_time = time.time() - start_time
                self.operations.append(operation)
            
            return response
            
        except Exception as e:
            LogManager.log_error("mcp", f"Error al procesar solicitud: {str(e)}")
            
            # Actualizar operación con error
            if operation:
                operation.error = {
                    "code": 500,
                    "message": str(e)
                }
                operation.execution_time = time.time() - start_time
                self.operations.append(operation)
            
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 500,
                    "message": f"Error interno: {str(e)}"
                },
                "id": request.get("id"),
                "version": request.get("version", "1.1")
            }
    
    async def _execute_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta una herramienta MCP
        
        Args:
            params: Parámetros de la herramienta
            
        Returns:
            Dict con el resultado
        """
        start_time = time.time()
        
        try:
            # Obtener herramienta
            tool_name = params.get("name")
            tool = self.tools.get(tool_name)
            
            if not tool:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 404,
                        "message": f"Herramienta no encontrada: {tool_name}"
                    }
                }
            
            # Verificar recursos requeridos
            for resource in tool.required_resources:
                if resource not in self.resources:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": 500,
                            "message": f"Recurso requerido no disponible: {resource}"
                        }
                    }
            
            # Verificar caché
            if tool.cache_enabled:
                cache_key = f"tool:{tool_name}:{json.dumps(params)}"
                cached_result = await self.cache_service.get(cache_key)
                if cached_result:
                    return {
                        "jsonrpc": "2.0",
                        "result": cached_result,
                        "cached": True
                    }
            
            # Ejecutar según la herramienta
            if tool_name == "buscar_en_brave":
                result = await self._execute_search(params)
            elif tool_name == "generar_markdown":
                result = await self._execute_markdown(params)
            elif tool_name == "analizar_texto":
                result = await self._execute_analysis(params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 501,
                        "message": f"Herramienta no implementada: {tool_name}"
                    }
                }
            
            # Guardar en caché
            if tool.cache_enabled:
                cache_key = f"tool:{tool_name}:{json.dumps(params)}"
                await self.cache_service.set(
                    cache_key,
                    result,
                    ttl=tool.cache_ttl or self.config.cache_ttl
                )
            
            return {
                "jsonrpc": "2.0",
                "result": result,
                "execution_time": time.time() - start_time
            }
            
        except Exception as e:
            LogManager.log_error("mcp", f"Error al ejecutar herramienta: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 500,
                    "message": f"Error al ejecutar herramienta: {str(e)}"
                }
            }
    
    async def _execute_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta la herramienta de búsqueda
        
        Args:
            params: Parámetros de búsqueda
            
        Returns:
            Dict con los resultados
        """
        query = params.get("query")
        num_results = params.get("num_results", 5)
        analyze = params.get("analyze", False)
        
        # Realizar búsqueda
        results = await self.resources_service.access_resource({
            "name": "search",
            "operation": "search",
            "parameters": {
                "query": query,
                "num_results": num_results
            }
        })
        
        # Analizar resultados si se solicita
        if analyze and results:
            analysis = await self.claude_service.analyze_text(
                text=json.dumps(results),
                analysis_type="search_results"
            )
            return {
                "results": results,
                "analysis": analysis
            }
        
        return results
    
    async def _execute_markdown(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta la herramienta de generación de Markdown
        
        Args:
            params: Parámetros de generación
            
        Returns:
            Dict con el resultado
        """
        content = params.get("content")
        format_type = params.get("format_type", "article")
        
        # Generar Markdown
        markdown = await self.claude_service.generate_markdown(
            content=content,
            format_type=format_type
        )
        
        # Guardar si se solicita
        if params.get("save", False):
            filename = params.get("filename", "output.md")
            await self.filesystem_service.save_file(markdown, filename)
            return {
                "content": markdown,
                "saved_as": filename
            }
        
        return {
            "content": markdown
        }
    
    async def _execute_analysis(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta la herramienta de análisis de texto
        
        Args:
            params: Parámetros de análisis
            
        Returns:
            Dict con el resultado
        """
        text = params.get("text")
        analysis_type = params.get("analysis_type", "summary")
        
        # Analizar texto
        result = await self.claude_service.analyze_text(
            text=text,
            analysis_type=analysis_type
        )
        
        return result
    
    async def get_recent_operations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene las operaciones recientes
        
        Args:
            limit: Número máximo de operaciones
            
        Returns:
            Lista de operaciones recientes
        """
        return [op.dict() for op in self.operations[-limit:]] 