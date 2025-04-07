from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    # BRAVE_API_KEY: str = os.getenv("BRAVE_API_KEY", "")
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    
    # Configuración del servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Configuración de directorios
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    LOG_DIR: Path = BASE_DIR / os.getenv("LOG_DIR", "logs")
    DATA_DIR: Path = BASE_DIR / os.getenv("DATA_DIR", "data")
    TEMP_DIR: Path = BASE_DIR / os.getenv("TEMP_DIR", "temp")
    
    # Configuración de Claude
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")
    CLAUDE_MAX_TOKENS: int = int(os.getenv("CLAUDE_MAX_TOKENS", "4096"))
    CLAUDE_TEMPERATURE: float = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
    
    # Configuración de búsqueda
    DEFAULT_SEARCH_RESULTS: int = int(os.getenv("DEFAULT_SEARCH_RESULTS", "5"))
    DEFAULT_SEARCH_COUNTRY: str = os.getenv("DEFAULT_SEARCH_COUNTRY", "ES")
    DEFAULT_SEARCH_LANGUAGE: str = os.getenv("DEFAULT_SEARCH_LANGUAGE", "es")
    
    # Configuración del sistema de archivos
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: List[str] = os.getenv("ALLOWED_EXTENSIONS", "md,txt,json").split(",")
    UPLOAD_DIR: Path = BASE_DIR / os.getenv("UPLOAD_DIR", "uploads")
    
    class Config:
        case_sensitive = True

# Instancia global de configuración
settings = Settings() 