from typing import Optional, Dict, Any
from fastapi import HTTPException
from app.core.logging import LogManager

class MCPClaudeError(Exception):
    """Clase base para excepciones de MCP Claude"""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)
        
        # Registrar el error
        LogManager.log_error(
            message,
            error=self,
            extra={
                "error_code": error_code,
                "status_code": status_code,
                "details": details
            }
        )

class ClaudeAPIError(MCPClaudeError):
    """Error en la comunicación con la API de Claude"""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status_code,
            error_code="CLAUDE_API_ERROR",
            details=details
        )

class ClaudeRateLimitError(ClaudeAPIError):
    """Error de límite de tasa de Claude"""
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=429,
            details=details
        )

class ClaudeAuthenticationError(ClaudeAPIError):
    """Error de autenticación con Claude"""
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=401,
            details=details
        )

class ClaudeValidationError(MCPClaudeError):
    """Error de validación de datos para Claude"""
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            details=details
        )

class ClaudeStreamingError(MCPClaudeError):
    """Error en el streaming de Claude"""
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code="STREAMING_ERROR",
            details=details
        ) 