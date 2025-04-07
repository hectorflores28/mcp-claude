# Guía de Instalación Detallada - MCP Claude

## Requisitos del Sistema

### Software Requerido
- Python 3.9 o superior
- Docker y Docker Compose (opcional)
- Redis 6.0 o superior
- Prometheus 2.0 o superior

### API Keys Necesarias
- Anthropic API Key (Claude)
- Brave Search API Key
- API Key personal para el servidor

## Instalación Local

### 1. Preparación del Entorno

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/mcp-claude.git
cd mcp-claude

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus claves
nano .env
```

Variables de entorno necesarias:
```env
ANTHROPIC_API_KEY=tu-api-key
BRAVE_SEARCH_API_KEY=tu-api-key
SERVER_API_KEY=tu-api-key
REDIS_HOST=localhost
REDIS_PORT=6379
PROMETHEUS_PORT=9090
LOG_LEVEL=INFO
```

### 3. Iniciar Servicios

#### Con Docker Compose (Recomendado)
```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# O en modo desarrollo
docker-compose -f docker-compose.dev.yml up --build
```

#### Sin Docker
```bash
# Iniciar Redis (si no está instalado)
redis-server

# Iniciar Prometheus (si no está instalado)
prometheus --config.file=prometheus.yml

# Iniciar la aplicación
uvicorn app.main:app --reload
```

## Verificación de la Instalación

### 1. Verificar Servicios

```bash
# Verificar API
curl http://localhost:8000/health

# Verificar Redis
redis-cli ping

# Verificar Prometheus
curl http://localhost:9090/-/healthy
```

### 2. Verificar API Keys

```bash
# Verificar Claude API
curl -X POST http://localhost:8000/api/claude/verify \
  -H "Authorization: Bearer tu-api-key"

# Verificar Brave Search
curl -X POST http://localhost:8000/api/search/verify \
  -H "Authorization: Bearer tu-api-key"
```

## Configuración Avanzada

### 1. Configuración de Logging

```python
# app/core/logging.py
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "logs/claude.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}
```

### 2. Configuración de Caché

```python
# app/core/cache.py
CACHE_CONFIG = {
    "enabled": True,
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": None,
    "ttl": 3600,  # 1 hora
    "prefix": "claude:"
}
```

### 3. Configuración de Métricas

```python
# app/core/metrics.py
METRICS_CONFIG = {
    "enabled": True,
    "prometheus_port": 9090,
    "labels": {
        "environment": "production",
        "application": "mcp-claude"
    }
}
```

## Solución de Problemas Comunes

### 1. Problemas de API Key

**Síntoma**: Error 401 Unauthorized
**Solución**: 
- Verificar que la API key esté correctamente configurada en .env
- Asegurar que la API key tenga los permisos necesarios
- Verificar que la cuenta tenga fondos suficientes
- Comprobar la configuración de cuotas en Anthropic Console

### 2. Problemas de Redis

**Síntoma**: Error de conexión a Redis
**Solución**:
- Verificar que Redis esté en ejecución
- Comprobar la configuración de host y puerto
- Verificar credenciales si están configuradas

### 3. Problemas de Prometheus

**Síntoma**: Métricas no disponibles
**Solución**:
- Verificar que Prometheus esté en ejecución
- Comprobar la configuración del puerto
- Verificar las reglas de firewall

## Actualización del Sistema

### 1. Actualizar Código

```bash
# Actualizar código
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt
```

### 2. Actualizar Docker

```bash
# Reconstruir imágenes
docker-compose build

# Reiniciar servicios
docker-compose down
docker-compose up -d
```

## Recursos Adicionales

- [Documentación de Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Documentación de Brave Search API](https://brave.com/search/api/)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Redis](https://redis.io/documentation)
- [Documentación de Prometheus](https://prometheus.io/docs/) 