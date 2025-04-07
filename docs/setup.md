# Instalación y Configuración de MCP-Claude

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta en Anthropic con API key
- Redis (para caché)
- Prometheus (para métricas)

## Instalación

### 1. Instalar con pip

```bash
pip install mcp-claude
```

### 2. Instalar desde el código fuente

```bash
git clone https://github.com/tu-usuario/mcp-claude.git
cd mcp-claude
pip install -e .
```

## Configuración Básica

### 1. Configurar API Key

```python
from mcp_claude import ClaudeClient

# Configurar API key directamente
client = ClaudeClient(api_key="tu-api-key")

# O usando variables de entorno
import os
client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))
```

### 2. Configurar Modelo por Defecto

```python
# Configurar modelo por defecto
client.set_default_model("claude-3-opus")

# Configurar temperatura por defecto
client.set_default_temperature(0.7)
```

## Configuración Avanzada

### 1. Configurar Caché

```python
from mcp_claude import ClaudeClient

client = ClaudeClient(
    api_key="tu-api-key",
    cache_config={
        "enabled": True,
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "password": "tu-contraseña",
        "ttl": 3600  # Tiempo de vida en segundos
    }
)
```

### 2. Configurar Métricas

```python
from mcp_claude import ClaudeClient

client = ClaudeClient(
    api_key="tu-api-key",
    metrics_config={
        "enabled": True,
        "prometheus_port": 9090,
        "labels": {
            "environment": "production",
            "application": "mi-app"
        }
    }
)
```

### 3. Configurar Logging

```python
from mcp_claude import ClaudeClient
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("claude.log"),
        logging.StreamHandler()
    ]
)

client = ClaudeClient(
    api_key="tu-api-key",
    logging_config={
        "level": "INFO",
        "file": "claude.log",
        "max_size": 10485760,  # 10MB
        "backup_count": 5
    }
)
```

## Configuración con Docker

### 1. Usar la Imagen Docker

```bash
docker pull mcp-claude:latest
docker run -e ANTHROPIC_API_KEY=tu-api-key mcp-claude:latest
```

### 2. Docker Compose

```yaml
version: '3'

services:
  app:
    image: mcp-claude:latest
    environment:
      - ANTHROPIC_API_KEY=tu-api-key
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - prometheus
  
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

## Configuración en Producción

### 1. Variables de Entorno

```bash
# .env
ANTHROPIC_API_KEY=tu-api-key
CLAUDE_DEFAULT_MODEL=claude-3-opus
CLAUDE_DEFAULT_TEMPERATURE=0.7
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=tu-contraseña
PROMETHEUS_PORT=9090
LOG_LEVEL=INFO
```

### 2. Cargar Variables de Entorno

```python
from dotenv import load_dotenv
import os

load_dotenv()

client = ClaudeClient(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    cache_config={
        "host": os.environ.get("REDIS_HOST"),
        "port": int(os.environ.get("REDIS_PORT")),
        "password": os.environ.get("REDIS_PASSWORD")
    },
    metrics_config={
        "prometheus_port": int(os.environ.get("PROMETHEUS_PORT"))
    },
    logging_config={
        "level": os.environ.get("LOG_LEVEL")
    }
)
```

## Verificación de la Configuración

### 1. Verificar Conexión

```python
# Verificar conexión a la API
status = client.check_connection()
print(f"Estado de conexión: {status}")

# Verificar conexión a Redis
cache_status = client.check_cache_status()
print(f"Estado de caché: {cache_status}")

# Verificar conexión a Prometheus
metrics_status = client.check_metrics_status()
print(f"Estado de métricas: {metrics_status}")
```

### 2. Verificar Configuración

```python
# Obtener configuración actual
config = client.get_config()
print(f"Configuración: {config}")

# Verificar modelo por defecto
default_model = client.get_default_model()
print(f"Modelo por defecto: {default_model}")

# Verificar temperatura por defecto
default_temperature = client.get_default_temperature()
print(f"Temperatura por defecto: {default_temperature}")
```

## Solución de Problemas de Configuración

### 1. Problemas de API Key

- Verifica que la API key sea correcta
- Asegúrate de que la API key tenga los permisos necesarios
- Verifica que la cuenta tenga fondos suficientes

### 2. Problemas de Caché

- Verifica que Redis esté en ejecución
- Comprueba la conectividad a Redis
- Verifica las credenciales de Redis

### 3. Problemas de Métricas

- Verifica que Prometheus esté en ejecución
- Comprueba la conectividad a Prometheus
- Verifica la configuración de Prometheus

## Próximos Pasos

- [API Reference](api_reference.md): Consulta la documentación completa de la API
- [Ejemplos](examples.md): Explora ejemplos de código para diferentes casos de uso
- [Casos de Uso](use_cases.md): Descubre los casos de uso óptimos para Claude 