# MCP Claude Server

Servidor MCP (Model Context Protocol) para Claude con integración de herramientas externas.

## Características principales

- ✅ Integración con Claude API
- ✅ Búsqueda web con Brave Search API
- ✅ Sistema de archivos local para gestión de documentos
- ✅ Soporte para creación y edición de archivos Markdown
- ✅ API RESTful basada en FastAPI
- ✅ Documentación automática con Swagger/OpenAPI
- ✅ Sistema de logging en Markdown
- ✅ Manejo de errores y validaciones
- ✅ Autenticación mediante API keys
- ✅ Protocolo JSON-RPC 2.0 para comunicación
- ✅ Soporte para Docker y Docker Compose
- ✅ Health checks para monitoreo
- ✅ Volúmenes persistentes para datos y logs
- ✅ Monitoreo de recursos del sistema
- ✅ Endpoints para gestión de prompts
- ✅ Sistema de logging avanzado

## Estado Actual del Proyecto

### Implementado ✅
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

### En Desarrollo 🚧
- Tests unitarios y de integración
- Mejoras en el sistema de logging
- Optimización de rendimiento
- Documentación detallada de uso
- Ejemplos de uso para cada funcionalidad principal

### Pendiente 📋
- Interfaz web de administración
- Sistema de caché
- Monitoreo y métricas avanzadas
- Integración con más modelos de Claude
- Soporte para más formatos de archivo
- Sistema de plugins

## Estructura del Proyecto

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

## Requisitos

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
- Docker y Docker Compose (opcional)

## Configuración

1. Clonar el repositorio
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

## Uso

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

## Endpoints Disponibles

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

### Protocolo JSON-RPC 2.0
- `POST /mcp/execute`: Endpoint principal para ejecutar herramientas MCP según el protocolo JSON-RPC 2.0

## Ejemplo de Uso del Protocolo JSON-RPC 2.0

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

## Desarrollo

- Los endpoints principales están en `app/api/endpoints/`
- La lógica de negocio en `app/services/`
- Esquemas y modelos en `app/schemas/`
- Configuración y utilidades en `app/core/`

## Seguridad

- Autenticación mediante API keys
- Validación de entrada en todos los endpoints
- Logging de operaciones críticas
- Sanitización de operaciones de filesystem
- Prevención de directory traversal
- Validación de nombres de archivo
- Restricción de extensiones permitidas
- Límite de tamaño de archivo

## Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

MIT
