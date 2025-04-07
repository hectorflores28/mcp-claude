from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List

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
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 