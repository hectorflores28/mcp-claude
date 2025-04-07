from pythonjsonlogger import jsonlogger
import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.markdown_logger import MarkdownLogger
import json
import time
from pathlib import Path

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_DIR / "app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("mcp-claude")

class ClaudeLogFormatter(logging.Formatter):
    """Formateador personalizado para logs de Claude en formato JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
            
        return json.dumps(log_data)

class LogManager:
    """Gestor de logs para MCP-Claude"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not LogManager._initialized:
            self.logger = logging.getLogger("mcp_claude")
            self.logger.setLevel(logging.INFO)
            LogManager._initialized = True
    
    @classmethod
    def setup_logger(cls, log_dir: str = "logs") -> None:
        """Configura el sistema de logs"""
        instance = cls()
        
        # Crear directorio de logs si no existe
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        # Handler para archivo
        file_handler = logging.FileHandler(
            log_path / f"mcp_claude_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setFormatter(ClaudeLogFormatter())
        instance.logger.addHandler(file_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ClaudeLogFormatter())
        instance.logger.addHandler(console_handler)
    
    @classmethod
    def log_api_request(cls, method: str, path: str, data: Optional[Dict[str, Any]] = None) -> None:
        """Registra una solicitud API"""
        instance = cls()
        extra_data = {
            "type": "api_request",
            "method": method,
            "path": path,
            "data": data
        }
        instance.logger.info("API Request", extra={"extra_data": extra_data})
    
    @classmethod
    def log_api_response(cls, method: str, path: str, status_code: int, response_time: float) -> None:
        """Registra una respuesta API"""
        instance = cls()
        extra_data = {
            "type": "api_response",
            "method": method,
            "path": path,
            "status_code": status_code,
            "response_time": response_time
        }
        instance.logger.info("API Response", extra={"extra_data": extra_data})
    
    @classmethod
    def log_claude_request(cls, prompt: str, model: str, max_tokens: int) -> None:
        """Registra una solicitud a Claude"""
        instance = cls()
        extra_data = {
            "type": "claude_request",
            "model": model,
            "max_tokens": max_tokens,
            "prompt_length": len(prompt)
        }
        instance.logger.info("Claude Request", extra={"extra_data": extra_data})
    
    @classmethod
    def log_claude_response(cls, model: str, response_time: float, token_count: int) -> None:
        """Registra una respuesta de Claude"""
        instance = cls()
        extra_data = {
            "type": "claude_response",
            "model": model,
            "response_time": response_time,
            "token_count": token_count
        }
        instance.logger.info("Claude Response", extra={"extra_data": extra_data})
    
    @classmethod
    def log_error(cls, error_type: str, error_message: str, stack_trace: Optional[str] = None) -> None:
        """Registra un error"""
        instance = cls()
        extra_data = {
            "type": "error",
            "error_type": error_type,
            "stack_trace": stack_trace
        }
        instance.logger.error(error_message, extra={"extra_data": extra_data})
    
    @classmethod
    def log_info(cls, message: str, **kwargs) -> None:
        """Registra un mensaje informativo"""
        instance = cls()
        instance.logger.info(message, extra={"extra_data": kwargs})
    
    @classmethod
    def log_warning(cls, message: str, **kwargs) -> None:
        """Registra un mensaje de advertencia"""
        instance = cls()
        instance.logger.warning(message, extra={"extra_data": kwargs})
    
    @classmethod
    def log_debug(cls, message: str, **kwargs) -> None:
        """Registra un mensaje de depuración"""
        instance = cls()
        instance.logger.debug(message, extra={"extra_data": kwargs})

    @classmethod
    def log_search(cls, query: str, results: list):
        """
        Registra una búsqueda
        """
        cls._logger.info(f"Search: {query} - Results: {len(results)}")
        cls._markdown_logger.log_search(query, results)
    
    @classmethod
    def log_file_operation(cls, operation: str, filename: str, details: str = None):
        """
        Registra una operación de archivo
        """
        message = f"File Operation: {operation} - File: {filename}"
        if details:
            message += f" - Details: {details}"
        cls._logger.info(message)
        cls._markdown_logger.log_file_operation(operation, filename, details)
    
    @classmethod
    def log_claude_operation(cls, operation: str, prompt: str, response: str):
        """
        Registra una operación de Claude
        """
        cls._logger.info(f"Claude Operation: {operation}")
        cls._markdown_logger.log_claude_operation(operation, prompt, response)

    @classmethod
    def log_model_request(
        cls,
        model: str,
        prompt: str,
        parameters: Dict[str, Any]
    ) -> None:
        """Registra una solicitud al modelo."""
        cls._logger.info(
            "Model Request",
            extra={
                "type": "model_request",
                "model": model,
                "prompt": prompt,
                "parameters": parameters
            }
        )
        cls._markdown_logger.log_model_request(model, prompt, parameters)

    @classmethod
    def log_info(cls, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Registra un mensaje informativo."""
        cls._logger.info(
            message,
            extra={"type": "info", "details": details}
        )
        cls._markdown_logger.log_info(message, details)

    @classmethod
    def log_warning(cls, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Registra una advertencia."""
        cls._logger.warning(
            message,
            extra={"type": "warning", "details": details}
        )
        cls._markdown_logger.log_warning(message, details) 