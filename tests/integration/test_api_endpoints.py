"""
Pruebas de integración para los endpoints de la API.

Este módulo contiene las pruebas de integración para los endpoints
de la API, incluyendo autenticación, operaciones MCP y plugins.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import jwt
from datetime import datetime, timedelta

client = TestClient(app)

def create_test_token() -> str:
    """
    Crea un token JWT de prueba.
    
    Returns:
        str: Token JWT
    """
    payload = {
        "sub": "test_user",
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

@pytest.fixture
def auth_headers() -> dict:
    """
    Fixture que proporciona headers de autenticación.
    
    Returns:
        dict: Headers de autenticación
    """
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}

def test_health_check(test_client: TestClient):
    """
    Prueba el endpoint de health check.
    
    Args:
        test_client: Fixture del cliente de prueba
    """
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "services" in data

def test_status_endpoint(test_client: TestClient):
    """
    Prueba el endpoint de status.
    
    Args:
        test_client: Fixture del cliente de prueba
    """
    response = test_client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
    assert "services" in data

def test_auth_token_endpoint(test_client: TestClient):
    """
    Prueba el endpoint de obtención de token.
    
    Args:
        test_client: Fixture del cliente de prueba
    """
    response = test_client.post(
        "/api/v1/auth/token",
        json={"username": "test_user", "password": "test_pass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_auth_token_invalid_credentials(test_client: TestClient):
    """
    Prueba el endpoint de token con credenciales inválidas.
    
    Args:
        test_client: Fixture del cliente de prueba
    """
    response = test_client.post(
        "/api/v1/auth/token",
        json={"username": "invalid", "password": "invalid"}
    )
    assert response.status_code == 401

def test_protected_endpoint_with_token(test_client: TestClient, auth_headers: dict):
    """
    Prueba un endpoint protegido con token válido.
    
    Args:
        test_client: Fixture del cliente de prueba
        auth_headers: Fixture de headers de autenticación
    """
    response = test_client.get("/api/v1/mcp/status", headers=auth_headers)
    assert response.status_code == 200

def test_protected_endpoint_without_token(test_client: TestClient):
    """
    Prueba un endpoint protegido sin token.
    
    Args:
        test_client: Fixture del cliente de prueba
    """
    response = test_client.get("/api/v1/mcp/status")
    assert response.status_code == 401

def test_rate_limit(test_client: TestClient, auth_headers: dict):
    """
    Prueba el rate limiting.
    
    Args:
        test_client: Fixture del cliente de prueba
        auth_headers: Fixture de headers de autenticación
    """
    # Realizar múltiples peticiones
    for _ in range(100):
        response = test_client.get("/api/v1/mcp/status", headers=auth_headers)
        assert response.status_code == 200
    
    # La siguiente petición debería fallar
    response = test_client.get("/api/v1/mcp/status", headers=auth_headers)
    assert response.status_code == 429

def test_auth_refresh_token(test_client: TestClient, auth_headers: dict):
    """
    Prueba el endpoint de refresh token.
    
    Args:
        test_client: Fixture del cliente de prueba
        auth_headers: Fixture de headers de autenticación
    """
    response = test_client.post("/api/v1/auth/refresh", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_auth_revoke_token(test_client: TestClient, auth_headers: dict):
    """
    Prueba el endpoint de revocación de token.
    
    Args:
        test_client: Fixture del cliente de prueba
        auth_headers: Fixture de headers de autenticación
    """
    response = test_client.post("/api/v1/auth/revoke", headers=auth_headers)
    assert response.status_code == 200
    
    # Intentar usar el token revocado
    response = test_client.get("/api/v1/mcp/status", headers=auth_headers)
    assert response.status_code == 401 