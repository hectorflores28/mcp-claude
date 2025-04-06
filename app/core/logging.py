import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from loguru import logger
from app.core.config import settings

# Configurar el logger
log_dir = settings.LOG_DIR
os.makedirs(log_dir, exist_ok=True)

# Configurar el logger para archivos
logger.add(
    os.path.join(log_dir, "app.log"),
    rotation="10 MB",
    retention="1 week",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Configurar el logger para errores
logger.add(
    os.path.join(log_dir, "error.log"),
    rotation="10 MB",
    retention="1 week",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

class LogManager:
    """Clase para gestionar los logs de la aplicación."""
    
    @staticmethod
    def log_operation(
        operation: str,
        details: Dict[str, Any],
        level: str = "INFO"
    ) -> None:
        """
        Registra una operación en el log.
        
        Args:
            operation: Tipo de operación
            details: Detalles de la operación
            level: Nivel de log (INFO, WARNING, ERROR)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details
        }
        
        # Registrar en el archivo de log
        log_file = os.path.join(log_dir, "operations.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Registrar con loguru
        if level == "INFO":
            logger.info(f"Operación: {operation} | Detalles: {details}")
        elif level == "WARNING":
            logger.warning(f"Operación: {operation} | Detalles: {details}")
        elif level == "ERROR":
            logger.error(f"Operación: {operation} | Detalles: {details}")
    
    @staticmethod
    def log_api_request(
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        status_code: int = 200
    ) -> None:
        """
        Registra una solicitud API.
        
        Args:
            method: Método HTTP
            path: Ruta de la API
            params: Parámetros de la solicitud
            status_code: Código de estado HTTP
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "path": path,
            "params": params or {},
            "status_code": status_code
        }
        
        # Registrar en el archivo de log
        log_file = os.path.join(log_dir, "api.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Registrar con loguru
        level = "INFO" if status_code < 400 else "WARNING" if status_code < 500 else "ERROR"
        if level == "INFO":
            logger.info(f"API: {method} {path} | Status: {status_code}")
        elif level == "WARNING":
            logger.warning(f"API: {method} {path} | Status: {status_code}")
        elif level == "ERROR":
            logger.error(f"API: {method} {path} | Status: {status_code}")
    
    @staticmethod
    def log_error(
        error_type: str,
        error_message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Registra un error.
        
        Args:
            error_type: Tipo de error
            error_message: Mensaje de error
            details: Detalles adicionales
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "details": details or {}
        }
        
        # Registrar en el archivo de log
        log_file = os.path.join(log_dir, "errors.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Registrar con loguru
        logger.error(f"Error: {error_type} | Mensaje: {error_message}") 