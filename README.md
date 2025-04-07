# 🚀 MCP-Claude

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-6.0+-red.svg)](https://redis.io/)
[![Tests](https://img.shields.io/badge/tests-60%25-yellow.svg)](https://github.com/tu-usuario/mcp-claude/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Servidor MCP (Model Context Protocol) para Claude Desktop v1.1.0 (Beta)

## 📋 Estado del Proyecto

| Métrica | Valor |
|---------|-------|
| Versión | 1.1.0 (Beta) |
| Estado | En desarrollo activo |
| Última actualización | 7 de abril de 2025 |
| Características implementadas | 80% |
| Tests implementados | 60% |

## ✨ Características Principales

- ✅ Protocolo MCP completo (v1.1)
- ✅ Sistema de recursos y herramientas
- ✅ Rate limiting con Redis
- ✅ Caché distribuido con Redis
- ✅ Logging avanzado con rotación de archivos
- ✅ Autenticación JWT y API Key
- ✅ Lista negra de tokens
- ✅ Configuración para Claude Desktop
- ✅ Tests unitarios y de integración

## 🛠️ Requisitos

- Python 3.10+
- Redis 6.0+
- XAMPP (para desarrollo local)

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/mcp-claude.git
cd mcp-claude

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables
cp .env.example .env
# Editar .env con tus configuraciones

# Iniciar Redis
redis-server

# Iniciar servidor
uvicorn app.main:app --reload
```

## ⚙️ Configuración

### Variables de Entorno Principales

| Variable | Descripción | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta para JWT | - |
| `API_KEY` | Clave API para autenticación | - |
| `REDIS_HOST` | Host de Redis | localhost |
| `REDIS_PORT` | Puerto de Redis | 6379 |
| `REDIS_PASSWORD`: Contraseña de Redis (opcional) | - | - |
| `REDIS_SSL`: Habilitar SSL para Redis (default: false) | - | - |
| `LOG_LEVEL` | Nivel de logging | INFO |
| `LOG_DIR`: Directorio de logs (default: logs) | - | - |
| `LOG_MAX_BYTES`: Tamaño máximo de archivo de log (default: 10MB) | - | - |
| `LOG_BACKUP_COUNT`: Número de archivos de backup (default: 5) | - | - |

### Claude Desktop

1. Copiar `claude_desktop_config.json` a la carpeta de configuración
2. Reiniciar Claude Desktop
3. El protocolo MCP estará disponible automáticamente

## 🔌 API Endpoints

### Autenticación
- `POST /api/v1/auth/token` - Obtener token JWT
- `POST /api/v1/auth/refresh` - Refrescar token
- `POST /api/v1/auth/revoke` - Revocar token

### MCP
- `GET /api/mcp/status` - Estado del protocolo MCP
- `POST /api/mcp/execute` - Ejecutar operación MCP
- `GET /api/mcp/operations` - Obtener operaciones recientes

## 🧪 Desarrollo

### Tests
```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app

# Ejecutar tests específicos
pytest tests/unit/test_mcp_service.py
```

### Linting
```bash
# Formatear código
black .

# Ordenar imports
isort .

# Verificar tipos
mypy .
```

## 📄 Licencia

MIT

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

Para más detalles, consulta nuestra [guía de contribución](CONTRIBUTING.md).
