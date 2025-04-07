# MCP-Claude

Middleware de Control y Procesamiento para Claude API.

## Estado del Proyecto

### Implementado ✅
- Estructura base del proyecto
- Integración con Claude API
- Sistema de logging con formato JSON
- Manejo de errores personalizado
- Sistema de caché con TTL
- Pruebas unitarias para:
  - Cliente de Claude
  - Sistema de archivos
  - Servicio de búsqueda
  - Servicio de caché
- Documentación de API
- Configuración de Docker

### En Progreso 🚧
- Sistema de métricas
- Mejoras en el sistema de caché
- Pruebas de integración
- Documentación de desarrollo

### Pendiente 📝
- Implementación de rate limiting
- Sistema de monitoreo en tiempo real
- Optimización de rendimiento
- Pruebas de carga
- Documentación de despliegue

## Estructura del Proyecto

```
mcp-claude/
├── app/
│   ├── api/
│   │   └── endpoints/
│   ├── core/
│   ├── services/
│   ├── schemas/
│   └── utils/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── data/
└── logs/
```

## Requisitos

- Python 3.8+
- FastAPI
- Claude API Key
- Docker (opcional)

## Instalación

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar variables de entorno (ver `.env.example`)
4. Ejecutar: `uvicorn app.main:app --reload`

## Uso

[Documentación de uso detallada]

## Contribución

[Guía de contribución]

## Licencia

MIT
