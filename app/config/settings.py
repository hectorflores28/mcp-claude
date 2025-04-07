from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List, Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "MCP-Claude"
    VERSION: str = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Claude API Configuration
    CLAUDE_API_KEY: str
    CLAUDE_MODEL: str = "claude-3-opus-20240229"
    CLAUDE_MAX_TOKENS: int = 4096
    CLAUDE_TEMPERATURE: float = 0.7
    
    # Search API Configuration
    BRAVE_SEARCH_API_KEY: str
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_DIR: Path = Path("logs")
    
    # File System Configuration
    DATA_DIR: Path = Path("data")
    
    # Configuración de Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    REDIS_SSL: bool = os.getenv("REDIS_SSL", "false").lower() == "true"
    
    # Configuración de caché
    CACHE_TTL: int = 300  # 5 minutos por defecto
    CACHE_PREFIX: str = "mcp:"
    
    # Configuración de rate limiting
    RATE_LIMIT_WINDOW: int = 60  # 1 minuto
    RATE_LIMIT_MAX_REQUESTS: int = 100
    
    # Configuración de JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    JWT_ALGORITHM: str = "HS256"
    JWT_ISSUER: str = "mcp-claude"
    JWT_AUDIENCE: str = "claude-desktop"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Configuración de seguridad
    API_KEY: str = os.getenv("API_KEY", "your-api-key-here")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Configuración del servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 