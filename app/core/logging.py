from pythonjsonlogger import jsonlogger
import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any
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
    _logger = None
    _log_dir = "logs"

    @classmethod
    def setup_logger(cls) -> None:
        """Configura el logger con formato JSON y múltiples handlers."""
        if cls._logger is not None:
            return

        # Crear directorio de logs si no existe
        os.makedirs(cls._log_dir, exist_ok=True)

        # Configurar logger
        cls._logger = logging.getLogger("mcp-claude")
        cls._logger.setLevel(logging.INFO)

        # Formato JSON personalizado
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d'
        )

        # Handler para archivo
        log_file = os.path.join(
            cls._log_dir,
            f"mcp_claude_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        cls._logger.addHandler(file_handler)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        cls._logger.addHandler(console_handler)

    @classmethod
    def log_info(cls, message: str, **kwargs):
        """
        Registra un mensaje informativo
        """
        cls._logger.info(message, **kwargs)
        cls._markdown_logger.log_info(message)
    
    @classmethod
    def log_error(cls, context: str, message: str, **kwargs):
        """
        Registra un error
        """
        cls._logger.error(f"[{context}] {message}", **kwargs)
        cls._markdown_logger.log_error(context, message)
    
    @classmethod
    def log_warning(cls, message: str, **kwargs):
        """
        Registra una advertencia
        """
        cls._logger.warning(message, **kwargs)
        cls._markdown_logger.log_warning(message)
    
    @classmethod
    def log_api_request(
        cls,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Registra una solicitud API."""
        cls._logger.info(
            "API Request",
            extra={
                "type": "api_request",
                "method": method,
                "path": path,
                "data": data
            }
        )
        cls._markdown_logger.log_api_request(method, path, data)
    
    @classmethod
    def log_api_response(
        cls,
        method: str,
        path: str,
        status_code: int,
        response_time: float
    ) -> None:
        """Registra una respuesta API."""
        cls._logger.info(
            "API Response",
            extra={
                "type": "api_response",
                "method": method,
                "path": path,
                "status_code": status_code,
                "response_time": response_time
            }
        )
        cls._markdown_logger.log_api_response(method, path, status_code, None)
    
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
    def log_error(
        cls,
        error_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Registra un error."""
        cls._logger.error(
            message,
            extra={
                "type": "error",
                "error_type": error_type,
                "details": details
            }
        )
        cls._markdown_logger.log_error(error_type, message, details)

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