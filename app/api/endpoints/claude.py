from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.core.security import verify_api_key
from app.services.claude_service import ClaudeService
from app.schemas.claude import (
    ClaudeRequest,
    ClaudeResponse,
    ClaudeAnalysis
)
from app.core.logging import LogManager
from app.core.markdown_logger import MarkdownLogger

router = APIRouter(prefix="/claude", tags=["claude"])
claude_service = ClaudeService()
markdown_logger = MarkdownLogger()

@router.get("/status")
async def claude_status(
    api_key: str = Depends(verify_api_key)
):
    """
    Verifica el estado del servicio de Claude.
    
    Args:
        api_key: API key para autenticación
        
    Returns:
        Dict: Estado del servicio
    """
    return {
        "status": "ok",
        "model": claude_service.model,
        "max_tokens": claude_service.max_tokens,
        "temperature": claude_service.temperature
    }

@router.post("/mcp/completion", response_model=ClaudeResponse)
async def mcp_completion(
    request: ClaudeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Endpoint específico para la integración con Claude Desktop MCP.
    
    Args:
        request: Solicitud de completado
        api_key: API key para autenticación
        
    Returns:
        ClaudeResponse: Respuesta de Claude
    """
    try:
        # Registrar la operación
        markdown_logger.log_claude_operation(
            operation="mcp_completion",
            details={
                "text": request.text[:100] + "..."
            }
        )
        
        # Realizar completado
        response = await claude_service.mcp_completion(
            prompt=request.text,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return ClaudeResponse(
            content=response["content"],
            tokens_used=response["tokens_used"],
            model=response["model"]
        )
        
    except Exception as e:
        LogManager.log_error("claude", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )

@router.post("/analyze", response_model=ClaudeResponse)
async def analyze_text(
    request: ClaudeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analiza texto usando Claude.
    
    Args:
        request: Solicitud de análisis
        api_key: API key para autenticación
        
    Returns:
        ClaudeResponse: Resultado del análisis
    """
    try:
        # Registrar la operación
        markdown_logger.log_claude_operation(
            operation="analyze",
            details={
                "text": request.text[:100] + "...",
                "analysis_type": request.analysis_type
            }
        )
        
        # Realizar análisis
        response = await claude_service.analyze_text(
            text=request.text,
            analysis_type=request.analysis_type,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return ClaudeResponse(
            content=response.content,
            tokens_used=response.tokens_used,
            model=response.model,
            analysis=response.analysis
        )
        
    except Exception as e:
        LogManager.log_error("claude", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar texto: {str(e)}"
        )

@router.post("/generate", response_model=ClaudeResponse)
async def generate_markdown(
    request: ClaudeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Genera contenido en formato Markdown usando Claude.
    
    Args:
        request: Solicitud de generación
        api_key: API key para autenticación
        
    Returns:
        ClaudeResponse: Contenido generado
    """
    try:
        # Registrar la operación
        markdown_logger.log_claude_operation(
            operation="generate",
            details={
                "text": request.text[:100] + "...",
                "format_type": request.format_type
            }
        )
        
        # Generar contenido
        response = await claude_service.generate_markdown(
            text=request.text,
            format_type=request.format_type,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return ClaudeResponse(
            content=response.content,
            tokens_used=response.tokens_used,
            model=response.model
        )
        
    except Exception as e:
        LogManager.log_error("claude", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar contenido: {str(e)}"
        ) 