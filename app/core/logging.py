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
    def setup_logger(cls) -> None:
        """Configura el sistema de logs"""
        # Crear directorio de logs si no existe
        log_path = Path(settings.LOG_DIR)
        log_path.mkdir(exist_ok=True, parents=True)
        
        # Configurar logger
        logger = logging.getLogger("mcp_claude")
        logger.setLevel(logging.INFO)
        
        # Limpiar handlers existentes
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Handler para archivo
        file_handler = logging.FileHandler(
            log_path / "app.log"
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(console_handler)
        
        # Registrar inicio
        logger.info("Sistema de logging inicializado")
    
    @classmethod
    def log_api_request(cls, method: str, path: str, data: Optional[Dict[str, Any]] = None) -> None:
        """Registra una solicitud API"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"API Request: {method} {path}")
        if data:
            logger.info(f"Request Data: {json.dumps(data)[:500]}...")
    
    @classmethod
    def log_api_response(cls, method: str, path: str, status_code: int, response_time: float) -> None:
        """Registra una respuesta API"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"API Response: {method} {path} - Status: {status_code} - Time: {response_time:.2f}s")
    
    @classmethod
    def log_claude_request(cls, prompt: str, model: str, max_tokens: int) -> None:
        """Registra una solicitud a Claude"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"Claude Request: Model: {model}, Max Tokens: {max_tokens}")
        logger.info(f"Prompt: {prompt[:200]}...")
    
    @classmethod
    def log_claude_response(cls, model: str, response_time: float, token_count: int) -> None:
        """Registra una respuesta de Claude"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"Claude Response: Model: {model}, Time: {response_time:.2f}s, Tokens: {token_count}")
    
    @classmethod
    def log_error(cls, error_type: str, error_message: str, stack_trace: Optional[str] = None) -> None:
        """Registra un error"""
        logger = logging.getLogger("mcp_claude")
        logger.error(f"Error: {error_type} - {error_message}")
        if stack_trace:
            logger.error(f"Stack Trace: {stack_trace}")
    
    @classmethod
    def log_info(cls, message: str, **kwargs) -> None:
        """Registra un mensaje informativo"""
        logger = logging.getLogger("mcp_claude")
        logger.info(message, **kwargs)
    
    @classmethod
    def log_warning(cls, message: str, **kwargs) -> None:
        """Registra un mensaje de advertencia"""
        logger = logging.getLogger("mcp_claude")
        logger.warning(message, **kwargs)
    
    @classmethod
    def log_debug(cls, message: str, **kwargs) -> None:
        """Registra un mensaje de depuración"""
        logger = logging.getLogger("mcp_claude")
        logger.debug(message, **kwargs)
    
    @classmethod
    def log_search(cls, query: str, results: list):
        """Registra una búsqueda"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"Search: {query} - Results: {len(results)}")
    
    @classmethod
    def log_file_operation(cls, operation: str, filename: str, details: str = None):
        """Registra una operación de archivo"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"File Operation: {operation} - {filename}")
        if details:
            logger.info(f"Details: {details}")
    
    @classmethod
    def log_claude_operation(cls, operation: str, prompt: str, response: str):
        """Registra una operación de Claude"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"Claude Operation: {operation}")
        logger.info(f"Prompt: {prompt[:200]}...")
        logger.info(f"Response: {response[:200]}...")
    
    @classmethod
    def log_model_request(
        cls,
        model: str,
        prompt: str,
        parameters: Dict[str, Any]
    ) -> None:
        """Registra una solicitud de modelo"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"Model Request: {model}")
        logger.info(f"Parameters: {json.dumps(parameters)}")
        logger.info(f"Prompt: {prompt[:200]}...")
    
    @classmethod
    def log_mcp_request(cls, endpoint: str, data: Dict[str, Any]) -> None:
        """Registra una solicitud MCP"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"MCP Request: {endpoint}")
        logger.info(f"Data: {json.dumps(data)[:500]}...")
    
    @classmethod
    def log_mcp_response(cls, endpoint: str, status: int, response_time: float) -> None:
        """Registra una respuesta MCP"""
        logger = logging.getLogger("mcp_claude")
        logger.info(f"MCP Response: {endpoint} - Status: {status} - Time: {response_time:.2f}s") 