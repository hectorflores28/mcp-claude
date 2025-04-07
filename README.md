# MCP Claude Server

Servidor MCP (Model Context Protocol) para Claude con integración de herramientas externas.

## 🚀 Características Principales

- 🤖 Integración con Claude API (Claude 3 Opus, Sonnet, Haiku)
- 🔍 Búsqueda web con Brave Search API
- 📁 Sistema de archivos local para gestión de documentos
- 📝 Soporte para creación y edición de archivos Markdown
- 🌐 API RESTful basada en FastAPI
- 📚 Documentación automática con Swagger/OpenAPI
- 📊 Sistema de logging en Markdown
- ⚠️ Manejo de errores y validaciones
- 🔐 Autenticación mediante API keys
- 🔄 Protocolo JSON-RPC 2.0 para comunicación
- 🐳 Soporte para Docker y Docker Compose
- 💓 Health checks para monitoreo
- 💾 Volúmenes persistentes para datos y logs
- 📈 Monitoreo de recursos del sistema
- 🎯 Endpoints para gestión de prompts
- 📊 Sistema de logging avanzado
- 🔄 Sistema de caché con Redis
- 📊 Métricas con Prometheus

## 📊 Estado Actual del Proyecto

### ✅ Implementado
- Estructura base del proyecto
- Esquemas Pydantic para todas las entidades
- Sistema de logging en Markdown
- Integración con Claude API
- Integración con Brave Search API
- Sistema de archivos local
- Manejo de errores y validaciones
- Autenticación básica
- Documentación API con Swagger
- Plantillas de prompts para Claude
- Configuración de variables de entorno
- Sistema de seguridad con API keys
- Sistema de caché con Redis
- Sistema de métricas con Prometheus
- Servicios principales:
  - BraveSearch: Búsqueda web con análisis de resultados
  - ClaudeService: Generación y análisis de contenido
  - FileSystemService: Gestión de archivos local
- Endpoints principales:
  - `/api/search`: Búsqueda web con Brave Search
  - `/api/filesystem`: Operaciones CRUD en archivos
  - `/api/tools`: Listado de herramientas MCP disponibles
  - `/api/tools/execute`: Ejecución de herramientas MCP
  - `/api/claude`: Operaciones de Claude
  - `/api/prompts`: Gestión de plantillas de prompts
  - `/api/logs`: Monitoreo de operaciones
  - `/api/health`: Monitoreo de salud del sistema
  - `/api/metrics`: Métricas del sistema
- Configuración Docker:
  - Dockerfile para producción
  - Docker Compose para desarrollo y producción
  - Health checks
  - Volúmenes persistentes
- Seguridad mejorada:
  - Validación de nombres de archivo
  - Prevención de directory traversal
  - Sanitización de entradas
  - Logging de operaciones críticas
- Monitoreo:
  - Verificación de salud de servicios
  - Monitoreo de recursos (CPU, memoria, disco)
  - Estadísticas de uso
  - Métricas de Prometheus

### 🚧 En Desarrollo
- Tests unitarios y de integración
- Mejoras en el sistema de logging
- Optimización de rendimiento
- Documentación detallada de uso
- Ejemplos de uso para cada funcionalidad principal
- Sistema de plugins
- Interfaz web de administración

### 📋 Pendiente
- Integración con más modelos de Claude
- Soporte para más formatos de archivo
- Sistema de plugins
- Interfaz web de administración

## 📁 Estructura del Proyecto

```
mcp-claude/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── search.py
│   │   │   ├── filesystem.py
│   │   │   ├── tools.py
│   │   │   ├── mcp.py
│   │   │   ├── claude.py
│   │   │   ├── prompts.py
│   │   │   ├── logs.py
│   │   │   └── health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   ├── prompts.py
│   │   ├── cache.py
│   │   ├── metrics.py
│   │   └── markdown_logger.py
│   ├── services/
│   │   ├── brave_search.py
│   │   ├── claude_service.py
│   │   └── filesystem_service.py
│   └── schemas/
│       ├── search.py
│       ├── filesystem.py
│       ├── claude.py
│       └── mcp.py
├── tests/
├── logs/
├── docs/
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## 📋 Requisitos

- Python 3.9+
- FastAPI
- Uvicorn
- Python-dotenv
- Anthropic (Claude API)
- Aiohttp
- Python-magic
- Aiofiles
- Pydantic
- Psutil
- Redis
- Prometheus Client
- Docker y Docker Compose (opcional)

## ⚙️ Configuración

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/mcp-claude.git
cd mcp-claude
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus claves API
```

## 🚀 Uso

### Desarrollo Local

1. Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

2. Acceder a la documentación API:
```
http://localhost:8000/docs
```

### Docker

1. Construir y ejecutar con Docker Compose:
```bash
# Producción
docker-compose up mcp-server

# Desarrollo (con hot-reload)
docker-compose up mcp-dev
```

2. Acceder a la documentación API:
```
http://localhost:8000/docs  # Producción
http://localhost:8001/docs  # Desarrollo
```

## 📚 Documentación

Para una documentación más detallada, consulta:

- [Guía de Instalación](docs/setup.md)
- [Ejemplos de Uso](docs/examples.md)
- [Casos de Uso](docs/use_cases.md)
- [Solución de Problemas](docs/troubleshooting.md)
- [Comparación con Gemini](docs/comparison.md)

## 🔄 Endpoints Disponibles

### Búsqueda Web
- `POST /api/search`: Realiza búsquedas web utilizando Brave Search API
  - Parámetros: query, num_results, country, language, analyze

### Sistema de Archivos
- `POST /api/filesystem`: Crea un nuevo archivo
- `GET /api/filesystem/{filename}`: Lee un archivo existente
- `GET /api/filesystem`: Lista todos los archivos disponibles
- `PUT /api/filesystem/{filename}`: Actualiza un archivo existente
- `DELETE /api/filesystem/{filename}`: Elimina un archivo existente

### Herramientas MCP
- `GET /api/tools`: Lista todas las herramientas MCP disponibles
- `POST /api/tools/execute`: Ejecuta una herramienta MCP específica

### Claude
- `POST /api/claude/analyze`: Analiza texto usando Claude
- `POST /api/claude/generate`: Genera contenido en formato Markdown

### Prompts
- `GET /api/prompts`: Lista todas las plantillas de prompts disponibles
- `GET /api/prompts/{name}`: Obtiene una plantilla específica
- `POST /api/prompts/{name}/format`: Formatea una plantilla con variables

### Logs
- `GET /api/logs/recent`: Obtiene los logs más recientes
- `GET /api/logs/search`: Busca logs por criterios específicos
- `GET /api/logs/stats`: Obtiene estadísticas de los logs

### Health
- `GET /api/health`: Verifica el estado general del servicio
- `GET /api/health/services`: Verifica el estado de los servicios individuales
- `GET /api/health/resources`: Verifica el uso de recursos del sistema

### Métricas
- `GET /api/metrics`: Obtiene métricas del sistema
- `GET /metrics`: Endpoint de Prometheus

### Protocolo JSON-RPC 2.0
- `POST /mcp/execute`: Endpoint principal para ejecutar herramientas MCP según el protocolo JSON-RPC 2.0

## 📝 Ejemplo de Uso del Protocolo JSON-RPC 2.0

```json
{
  "jsonrpc": "2.0",
  "method": "execute_tool",
  "params": {
    "tool_name": "buscar_en_brave",
    "parameters": {
      "query": "últimas noticias de IA",
      "num_results": 5,
      "analyze": true
    }
  },
  "id": 1
}
```

## 👩‍💻 Desarrollo

- Los endpoints principales están en `app/api/endpoints/`
- La lógica de negocio en `app/services/`
- Esquemas y modelos en `app/schemas/`
- Configuración y utilidades en `app/core/`

## 🔒 Seguridad

- Autenticación mediante API keys
- Validación de nombres de archivo
- Prevención de directory traversal
- Sanitización de entradas
- Logging de operaciones críticas
- Rate limiting
- CORS configurado
- Headers de seguridad

## 📊 Monitoreo

- Health checks
- Métricas de Prometheus
- Logging en Markdown
- Monitoreo de recursos
- Estadísticas de uso

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
