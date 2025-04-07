from pythonjsonlogger import jsonlogger
import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.markdown_logger import MarkdownLogger
import json
import time
from pathlib import Path

# Asegurar que el directorio de logs existe
log_dir = Path(settings.LOG_DIR)
log_dir.mkdir(exist_ok=True, parents=True)

# Obtener el nivel de logging
try:
    log_level = getattr(logging, settings.LOG_LEVEL.upper())
except AttributeError:
    log_level = logging.INFO
    print(f"Advertencia: Nivel de logging '{settings.LOG_LEVEL}' no válido. Usando INFO.")

# Configurar logging básico
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "app.log", mode='a', encoding='utf-8'),
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
    _logger = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls) -> None:
        """
        Inicializa el sistema de logging con configuración personalizada
        """
        if cls._initialized:
            return

        # Crear directorio de logs si no existe
        log_dir = settings.LOG_DIR
        os.makedirs(log_dir, exist_ok=True)

        # Configurar logger principal
        logger = logging.getLogger("mcp_claude")
        logger.setLevel(getattr(logging, settings.LOG_LEVEL))

        # Formato de logging
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Handler para archivo con rotación
        log_file = os.path.join(log_dir, "app.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        cls._logger = logger
        cls._initialized = True

        # Log inicial
        cls.log_info("Sistema de logging inicializado")
        cls.log_info(f"Directorio de logs: {log_dir}")
        cls.log_info(f"Nivel de logging: {settings.LOG_LEVEL}")
    
    @classmethod
    def log_info(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Registra un mensaje de nivel INFO
        """
        if not cls._initialized:
            cls.initialize()
        cls._logger.info(message, extra=extra or {})
    
    @classmethod
    def log_error(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Registra un mensaje de nivel ERROR
        """
        if not cls._initialized:
            cls.initialize()
        cls._logger.error(message, extra=extra or {})
    
    @classmethod
    def log_warning(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Registra un mensaje de nivel WARNING
        """
        if not cls._initialized:
            cls.initialize()
        cls._logger.warning(message, extra=extra or {})
    
    @classmethod
    def log_debug(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Registra un mensaje de nivel DEBUG
        """
        if not cls._initialized:
            cls.initialize()
        cls._logger.debug(message, extra=extra or {})
    
    @classmethod
    def log_request(cls, method: str, url: str, status_code: int, process_time: float) -> None:
        """
        Registra información de una solicitud HTTP
        """
        extra = {
            "method": method,
            "url": url,
            "status_code": status_code,
            "process_time": f"{process_time:.3f}s"
        }
        
        if status_code >= 500:
            cls.log_error(f"Error en solicitud: {method} {url}", extra)
        elif status_code >= 400:
            cls.log_warning(f"Solicitud fallida: {method} {url}", extra)
        else:
            cls.log_info(f"Solicitud exitosa: {method} {url}", extra)
    
    @classmethod
    def is_available(cls) -> bool:
        """
        Verifica si el sistema de logging está disponible
        """
        return cls._initialized and cls._logger is not None
    
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