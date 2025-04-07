import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import os
from pathlib import Path

@pytest.fixture
def test_client():
    """Fixture para el cliente de pruebas de FastAPI"""
    return TestClient(app)

@pytest.fixture
def test_env():
    """Fixture para variables de entorno de prueba"""
    os.environ["CLAUDE_API_KEY"] = "test_claude_key"
    os.environ["BRAVE_SEARCH_API_KEY"] = "test_brave_key"
    return {
        "CLAUDE_API_KEY": "test_claude_key",
        "BRAVE_SEARCH_API_KEY": "test_brave_key"
    }

@pytest.fixture
def test_data_dir():
    """Fixture para directorio de datos de prueba"""
    test_dir = Path("tests/data")
    test_dir.mkdir(exist_ok=True)
    return test_dir

@pytest.fixture
def test_log_dir():
    """Fixture para directorio de logs de prueba"""
    test_dir = Path("tests/logs")
    test_dir.mkdir(exist_ok=True)
    return test_dir

@pytest.fixture
def mock_claude_response():
    """Fixture para respuestas simuladas de Claude"""
    return {
        "content": "Test response from Claude",
        "model": settings.CLAUDE_MODEL,
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }

@pytest.fixture
def mock_search_response():
    """Fixture para respuestas simuladas de búsqueda"""
    return {
        "results": [
            {
                "title": "Test Result",
                "url": "https://test.com",
                "snippet": "Test snippet"
            }
        ]
    } 