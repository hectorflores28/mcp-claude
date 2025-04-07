# MCP-Claude

Middleware de Control y Procesamiento para Claude API.

## Estado del Proyecto

### FASE 1 - Estructura Similar

#### Implementado ✅
- Estructura base del proyecto
- Integración con Claude API
- Sistema de caché básico con TTL
- Pruebas unitarias básicas para:
  - Cliente de Claude
  - Sistema de archivos
  - Servicio de búsqueda
  - Servicio de caché

#### En Progreso 🚧
- Estructura de directorios mejorada
- Sistema de logs estandarizado
- Pruebas unitarias completas
- Documentación de desarrollo

#### Pendiente 📝
- Implementación de subdirectorios en core/
- Organización de servicios por tipo
- Sistema de rotación de logs
- Pruebas de integración
- Fixtures comunes
- Mocks específicos para Claude

### FASE 2 - Mejoras de API

#### Pendiente 📝
- Sistema de manejo de errores
- Caché avanzado
- Sistema de métricas
- Rate limiting
- Monitoreo en tiempo real

## Estructura del Proyecto

```
mcp-claude/
├── app/
│   ├── api/
│   │   └── endpoints/
│   ├── core/
│   │   ├── config/
│   │   ├── security/
│   │   └── logging/
│   ├── services/
│   │   ├── ai/
│   │   ├── cache/
│   │   ├── filesystem/
│   │   └── metrics/
│   ├── schemas/
│   └── utils/
├── tests/
│   ├── unit/
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── test_utils/
│   └── integration/
├── docs/
│   ├── api/
│   ├── development/
│   └── deployment/
├── data/
│   ├── cache/
│   └── models/
└── logs/
    ├── app/
    ├── access/
    └── error/
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
