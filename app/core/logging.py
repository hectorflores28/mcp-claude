import logging
from datetime import datetime
from pathlib import Path
from app.core.config import settings
from app.core.markdown_logger import MarkdownLogger

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

class LogManager:
    """
    Gestor centralizado de logs
    """
    _markdown_logger = MarkdownLogger()
    
    @classmethod
    def log_info(cls, message: str, **kwargs):
        """
        Registra un mensaje informativo
        """
        logger.info(message, **kwargs)
        cls._markdown_logger.log_info(message)
    
    @classmethod
    def log_error(cls, context: str, message: str, **kwargs):
        """
        Registra un error
        """
        logger.error(f"[{context}] {message}", **kwargs)
        cls._markdown_logger.log_error(context, message)
    
    @classmethod
    def log_warning(cls, message: str, **kwargs):
        """
        Registra una advertencia
        """
        logger.warning(message, **kwargs)
        cls._markdown_logger.log_warning(message)
    
    @classmethod
    def log_api_request(cls, method: str, path: str, data: dict = None):
        """
        Registra una solicitud API
        """
        message = f"API Request: {method} {path}"
        if data:
            message += f" - Data: {data}"
        logger.info(message)
        cls._markdown_logger.log_api_request(method, path, data)
    
    @classmethod
    def log_api_response(cls, method: str, path: str, status_code: int, data: dict = None):
        """
        Registra una respuesta API
        """
        message = f"API Response: {method} {path} - Status: {status_code}"
        if data:
            message += f" - Data: {data}"
        logger.info(message)
        cls._markdown_logger.log_api_response(method, path, status_code, data)
    
    @classmethod
    def log_search(cls, query: str, results: list):
        """
        Registra una búsqueda
        """
        logger.info(f"Search: {query} - Results: {len(results)}")
        cls._markdown_logger.log_search(query, results)
    
    @classmethod
    def log_file_operation(cls, operation: str, filename: str, details: str = None):
        """
        Registra una operación de archivo
        """
        message = f"File Operation: {operation} - File: {filename}"
        if details:
            message += f" - Details: {details}"
        logger.info(message)
        cls._markdown_logger.log_file_operation(operation, filename, details)
    
    @classmethod
    def log_claude_operation(cls, operation: str, prompt: str, response: str):
        """
        Registra una operación de Claude
        """
        logger.info(f"Claude Operation: {operation}")
        cls._markdown_logger.log_claude_operation(operation, prompt, response) 