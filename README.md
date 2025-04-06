# MCP-Claude

Implementación de un servidor MCP (Model Context Protocol) personalizado utilizando Claude como LLM principal.

## Características Principales

- ✅ Integración con Claude API
- ✅ Búsqueda web mediante Brave Search API
- ✅ Sistema de archivos local para gestión de documentos
- ✅ Soporte para creación y edición de archivos Markdown
- ✅ API RESTful basada en FastAPI
- ✅ Documentación automática con Swagger/OpenAPI
- ✅ Sistema de logging en Markdown
- ✅ Manejo de errores y validaciones
- ✅ Autenticación mediante API keys
- ✅ Protocolo JSON-RPC 2.0 para comunicación

## Estado Actual del Proyecto

### Implementado ✅
- Estructura base del proyecto
- Esquemas Pydantic para todas las entidades
- Endpoints principales (tools, search, filesystem)
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

### En Desarrollo 🚧
- Tests unitarios y de integración
- Mejoras en el sistema de logging
- Optimización de rendimiento
- Documentación detallada de uso
- Implementación de servicios (brave_search, claude_service, filesystem_service)
- Implementación de endpoints (search, filesystem, tools)

### Pendiente 📋
- Interfaz web de administración
- Sistema de caché
- Monitoreo y métricas
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
│   │   │   └── tools.py
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
│       └── mcp.py
├── tests/
├── logs/
├── docs/
├── .env.example
├── requirements.txt
└── docker-compose.yml
```

## Requisitos

- Python 3.9+
- FastAPI
- Uvicorn
- Python-dotenv
- Requests
- Docker (opcional)

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

1. Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

2. Acceder a la documentación API:
```
http://localhost:8000/docs
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

## Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

MIT
