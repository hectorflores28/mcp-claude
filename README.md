# MCP-Claude

Sistema de gestión de prompts para Claude 3.5 Sonnet.

## Estado Actual

### Implementado
- ✅ Estructura base del proyecto
- ✅ Configuración de Docker y Docker Compose
- ✅ Sistema de logs estandarizado
- ✅ Pruebas unitarias para:
  - ✅ ClaudeClient
  - ✅ FileSystemService
  - ✅ SearchService
  - ✅ CacheService
  - ✅ Sistema de logs
- ✅ Servicios principales:
  - ✅ Sistema de caché
  - ✅ Sistema de búsqueda
  - ✅ Sistema de archivos
  - ✅ Sistema de logs

### En Progreso
- 🔄 Integración con API de Claude
- 🔄 Sistema de gestión de prompts
- 🔄 Interfaz de usuario

### Pendiente
- ⏳ Sistema de autenticación
- ⏳ Sistema de monitoreo
- ⏳ Documentación completa
- ⏳ Pruebas de integración
- ⏳ Pruebas de rendimiento
- ⏳ Despliegue en producción

## Requisitos

- Python 3.10+
- Docker y Docker Compose
- API Key de Claude

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/mcp-claude.git
cd mcp-claude
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar con Docker:
```bash
docker-compose up -d
```

## Estructura del Proyecto

```
mcp-claude/
├── app/
│   ├── api/
│   ├── core/
│   │   ├── config/
│   │   ├── logging/
│   │   └── security/
│   ├── models/
│   ├── services/
│   └── utils/
├── data/
│   ├── prompts/
│   └── cache/
├── docs/
├── logs/
│   ├── app/
│   ├── access/
│   └── error/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Uso

```python
from app.services.claude_client import ClaudeClient

client = ClaudeClient(api_key="tu-api-key")
response = client.generate("Tu prompt aquí")
print(response)
```

## Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas unitarias
pytest tests/unit

# Ejecutar pruebas de integración
pytest tests/integration

# Ejecutar pruebas e2e
pytest tests/e2e
```

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
