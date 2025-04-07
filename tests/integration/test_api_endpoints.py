import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import jwt
from datetime import datetime, timedelta

client = TestClient(app)

def create_test_token():
    """Crea un token JWT de prueba"""
    payload = {
        "sub": "test_user",
        "type": "access_token",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

@pytest.fixture
def auth_headers():
    """Fixture para crear headers de autenticación"""
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}

def test_health_check():
    """Prueba el endpoint de salud"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "services" in data

def test_status_endpoint():
    """Prueba el endpoint de estado"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
    assert "services" in data

def test_auth_token_endpoint():
    """Prueba el endpoint de obtención de token"""
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "api",
            "password": settings.API_KEY
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_auth_token_invalid_credentials():
    """Prueba el endpoint de token con credenciales inválidas"""
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "api",
            "password": "invalid_key"
        }
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_protected_endpoint_with_token(auth_headers):
    """Prueba un endpoint protegido con token válido"""
    response = client.get("/api/mcp/status", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "features" in data

def test_protected_endpoint_without_token():
    """Prueba un endpoint protegido sin token"""
    response = client.get("/api/mcp/status")
    assert response.status_code == 401
    assert "detail" in response.json()

def test_rate_limit():
    """Prueba el límite de tasa"""
    # Realizar múltiples solicitudes para exceder el límite
    for _ in range(settings.RATE_LIMIT_MAX_REQUESTS + 1):
        response = client.get("/health")
        if response.status_code != 200:
            break
    
    assert response.status_code == 429
    assert "detail" in response.json()
    assert "Rate limit exceeded" in response.json()["detail"]

def test_auth_refresh_token(auth_headers):
    """Prueba el endpoint de refresco de token"""
    response = client.post("/api/v1/auth/refresh", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_auth_revoke_token(auth_headers):
    """Prueba el endpoint de revocación de token"""
    response = client.post("/api/v1/auth/revoke", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Token revocado correctamente" in data["message"] 