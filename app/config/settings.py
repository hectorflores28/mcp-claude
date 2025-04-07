from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Configuración general
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    VERSION: str = "1.1.0"
    PROJECT_NAME: str = "MCP-Claude"
    
    # Configuración del servidor
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    API_PREFIX: str = "/api"
    CORS_ORIGINS: str = "http://127.0.0.1:3000,http://127.0.0.1:8000"
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Configuración de seguridad
    API_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Configuración de Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SSL: bool = False
    
    # Configuración de caché
    CACHE_TTL: int = 300  # 5 minutos
    CACHE_PREFIX: str = "mcp:"
    
    # Configuración de rate limiting
    RATE_LIMIT_WINDOW: int = 60  # 1 minuto
    RATE_LIMIT_MAX_REQUESTS: int = 100
    
    # Configuración de Claude
    CLAUDE_API_KEY: str
    CLAUDE_MODEL: str = "claude-3-opus-20240229"
    CLAUDE_MAX_TOKENS: int = 4096
    CLAUDE_TEMPERATURE: float = 0.7
    
    # Configuración de Brave Search
    BRAVE_SEARCH_API_KEY: Optional[str] = None
    BRAVE_SEARCH_BASE_URL: str = "https://api.search.brave.com/res/v1/web/search"
    
    # Configuración de sistema de archivos
    DATA_DIR: str = "data"
    TEMP_DIR: str = "temp"
    ALLOWED_EXTENSIONS: List[str] = ["md", "txt", "json"]
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Crear directorios necesarios
        for directory in [self.LOG_DIR, self.DATA_DIR, self.TEMP_DIR]:
            os.makedirs(directory, exist_ok=True)

settings = Settings() 