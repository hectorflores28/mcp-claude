# 🚀 MCP-Claude

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green.svg)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-6.0+-red.svg)](https://redis.io/)
[![Tests](https://img.shields.io/badge/tests-75%25-yellow.svg)](https://github.com/hectorflores28/mcp-claude/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Servidor MCP (Model Context Protocol) para Claude Desktop v1.1.0 (Beta)

## 📋 Estado del Proyecto

| Métrica | Valor |
|---------|-------|
| Versión | 1.1.3 (Release Candidate) |
| Estado | ✅ Listo para Integración |
| Última actualización | 7 de abril de 2025 |
| Características implementadas | 95% |
| Tests implementados | 75% |

## ✨ Características Implementadas

- ✅ Protocolo MCP completo (v1.1)
- ✅ Sistema de recursos y herramientas
- ✅ Rate limiting con Redis
- ✅ Caché distribuido con Redis
- ✅ Logging avanzado con rotación de archivos
- ✅ Autenticación JWT y API Key
- ✅ Sistema de plugins para extensibilidad
- ✅ Configuración para Claude Desktop
- ✅ Tests unitarios y de integración
- ✅ Sistema de blacklist de tokens
- ✅ Métricas de rendimiento con Prometheus
- ✅ Procesamiento en lote para operaciones múltiples
- ✅ Cliente Claude con caché y reintentos
- ✅ Optimización de servicios y endpoints
- ✅ Validación de esquemas

## 🔄 Próximos Pasos

- ▶️ Pruebas de integración con Claude Desktop
- ▶️ Optimización de rendimiento en entorno real
- ▶️ Documentación de flujos de trabajo
- ▶️ Pruebas de carga y estrés

## 🛠️ Requisitos

- Python 3.11+
- Redis 6.0+
- XAMPP (para desarrollo local)
- Visual Studio Build Tools (para Windows)
- Rust (para compilación de dependencias)

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/hectorflores28/mcp-claude.git
cd mcp-claude

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

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

### Requisitos Adicionales para Windows

1. Instalar Visual Studio Build Tools:
```bash
winget install Microsoft.VisualStudio.2022.BuildTools
```

2. Instalar Rust:
```bash
winget install Rustlang.Rust.MSVC
```

3. Instalar Redis:
```bash
winget install Redis
```

## ⚙️ Configuración

### Variables de Entorno Principales

| Variable | Descripción | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta para JWT | - |
| `API_KEY` | Clave API para autenticación | - |
| `REDIS_HOST` | Host de Redis | localhost |
| `REDIS_PORT` | Puerto de Redis | 6379 |
| `REDIS_DB` | Base de datos Redis | 0 |
| `REDIS_PASSWORD` | Contraseña de Redis | - |
| `REDIS_SSL` | Habilitar SSL para Redis | false |
| `REDIS_TIMEOUT` | Timeout de conexión (segundos) | 5 |
| `REDIS_MAX_CONNECTIONS` | Máximo de conexiones | 10 |
| `LOG_LEVEL` | Nivel de logging | INFO |
| `LOG_DIR` | Directorio de logs | logs |
| `LOG_MAX_BYTES` | Tamaño máximo de archivo de log | 10MB |
| `LOG_BACKUP_COUNT` | Número de archivos de backup | 5 |
| `PLUGINS_ENABLED` | Habilitar sistema de plugins | true |
| `PLUGIN_DIR` | Directorio de plugins | plugins |

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

### Plugins
- `GET /api/v1/plugins` - Listar plugins disponibles
- `GET /api/v1/plugins/{plugin_id}` - Obtener información de un plugin
- `POST /api/v1/plugins/{plugin_id}/enable` - Habilitar un plugin
- `POST /api/v1/plugins/{plugin_id}/disable` - Deshabilitar un plugin

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

## 📝 Historial de Cambios

### v1.1.3 (7 de abril de 2025)
- Preparación para integración con Claude Desktop
- Optimización del cliente Claude con caché y reintentos
- Mejora de la validación de esquemas
- Optimización de servicios y endpoints
- Corrección de errores y mejoras de rendimiento

### v1.1.2 (7 de abril de 2025)
- Optimización del sistema de caché con pool de conexiones
- Implementación de blacklist de tokens con limpieza automática
- Mejora del sistema de métricas con procesamiento en lote
- Optimización del sistema de logging con formato JSON
- Implementación de reintentos automáticos para operaciones críticas
- Mejora del manejo de errores y excepciones

### v1.1.1 (7 de abril de 2025)
- Implementación del sistema de caché distribuido con Redis
- Mejora del sistema de logging con rotación de archivos
- Implementación del sistema de plugins para extensibilidad
- Configuración centralizada del proyecto
- Implementación de pruebas unitarias y de integración
- Documentación actualizada de API y endpoints

### v1.1.0 (7 de abril de 2025)
- Versión inicial del servidor MCP para Claude Desktop
- Implementación de la estructura base con FastAPI
- Sistema de autenticación con API Key y JWT
- Endpoints básicos para Claude Desktop MCP

### v1.0.0 (1 de abril de 2025)
- Versión inicial del servidor MCP para Claude Desktop
- Implementación de la estructura base con FastAPI
- Sistema de autenticación con API Key y JWT
- Endpoints básicos para Claude Desktop MCP
