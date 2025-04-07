from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from app.core.security import verify_api_key
from app.core.logging import LogManager
from app.services.mcp_service import MCPService
from app.schemas.mcp import MCPStatus, MCPOperation

router = APIRouter(prefix="/mcp", tags=["mcp"])
mcp_service = MCPService()

@router.get("/status", response_model=MCPStatus)
async def mcp_status(api_key: str = Depends(verify_api_key)):
    """
    Obtiene el estado del protocolo MCP
    """
    try:
        status = await mcp_service.get_status()
        LogManager.log_info("Estado del protocolo MCP obtenido")
        return status
    except Exception as e:
        LogManager.log_error("mcp", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute")
async def execute_mcp(request: Dict[str, Any], api_key: str = Depends(verify_api_key)):
    """
    Ejecuta una solicitud MCP
    """
    try:
        # Registrar solicitud
        LogManager.log_mcp_request(
            endpoint="/api/mcp/execute",
            data=request
        )
        
        # Procesar solicitud
        response = await mcp_service.process_request(request)
        
        # Registrar respuesta
        LogManager.log_mcp_response(
            endpoint="/api/mcp/execute",
            status=200 if "error" not in response else response["error"]["code"],
            response_time=response.get("execution_time", 0)
        )
        
        return response
    except Exception as e:
        LogManager.log_error("mcp", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/operations", response_model=List[Dict[str, Any]])
async def get_recent_operations(
    limit: int = 10,
    api_key: str = Depends(verify_api_key)
):
    """
    Obtiene las operaciones MCP recientes
    """
    try:
        operations = await mcp_service.get_recent_operations(limit)
        LogManager.log_info(f"Obtenidas {len(operations)} operaciones recientes")
        return operations
    except Exception as e:
        LogManager.log_error("mcp", str(e))
        raise HTTPException(status_code=500, detail=str(e)) 