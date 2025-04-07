# MCP-Claude

Sistema de integración con Claude 3.5 Sonnet para Claude Desktop, implementando el Model Context Protocol (MCP).

## Estado del Proyecto

### Versión Actual
- Versión: 1.1.0 (Beta)
- Estado: En desarrollo activo
- Última actualización: 2024-04-07

### Implementado ✅
- Estructura base del proyecto
- Configuración de FastAPI
- Sistema de logs estandarizado
- Integración básica con API de Claude
- Endpoints para Claude Desktop MCP
- Sistema de archivos básico
- Autenticación con API Key
- Endpoint de estado MCP
- Sistema de logging básico
- Protocolo MCP completo (v1.1)
- Sistema de recursos y herramientas
- Límite de tasa por método/herramienta
- Sistema de caché para resultados
- Registro de operaciones
- Configuración para Claude Desktop

### En Desarrollo 🔄
- Mejora de la integración con Claude Desktop
- Optimización del sistema de logs
- Documentación de API
- Pruebas unitarias y de integración
- Mejoras de seguridad avanzadas

### Próximas Versiones
- v1.2.0: Mejoras de seguridad y rendimiento
- v1.3.0: Documentación completa y pruebas
- v2.0.0: Versión estable para producción

Para ver la lista completa de tareas pendientes, consulta [PENDING.md](PENDING.md).

## Requisitos

- Python 3.10+
- API Key de Claude
- Claude Desktop
- Docker (opcional, para desarrollo)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/hectorflores28/mcp-claude.git
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

4. Crear directorios necesarios:
```bash
mkdir logs data temp uploads
```

5. Ejecutar el servidor:
```bash
python -m app.main
```

### Usando Docker

```bash
docker-compose up -d
```

## Integración con Claude Desktop

1. Configurar Claude Desktop:
   - Abrir Claude Desktop
   - Ir a Settings > Developers
   - Configurar MCP:
     ```json
     {
         "mcp": {
             "enabled": true,
             "url": "http://127.0.0.1:8000",
             "api_key": "tu-api-key-aquí"
         }
     }
     ```

2. Verificar la conexión:
   - Acceder a `http://127.0.0.1:8000/api/health`
   - Acceder a `http://127.0.0.1:8000/api/mcp/status`

3. Reiniciar Claude Desktop después de la configuración

## Estructura del Proyecto

```
mcp-claude/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       ├── claude.py
│   │       ├── filesystem.py
│   │       ├── mcp.py
│   │       └── ...
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── mcp_config.py
│   │   └── security.py
│   ├── schemas/
│   │   ├── mcp.py
│   │   └── ...
│   ├── services/
│   │   ├── claude_service.py
│   │   ├── mcp_service.py
│   │   └── ...
│   └── main.py
├── data/
├── logs/
├── temp/
├── uploads/
├── tests/
├── docs/
├── .env
├── claude_desktop_config.json
└── requirements.txt
```

## Endpoints Principales

- `/api/health` - Estado del servidor
- `/api/mcp/status` - Estado para integración con Claude Desktop
- `/api/mcp/execute` - Ejecución de herramientas MCP
- `/api/mcp/operations` - Consulta de operaciones recientes
- `/api/claude/status` - Estado del servicio de Claude
- `/api/claude/mcp/completion` - Endpoint para completado de Claude

## Características del Protocolo MCP

### Versión 1.1
- Soporte para múltiples versiones del protocolo
- Sistema de recursos con tipos y niveles de acceso
- Herramientas con parámetros y recursos requeridos
- Límite de tasa por método/herramienta
- Sistema de caché para resultados
- Registro de operaciones con timestamps
- Validación de solicitudes y respuestas
- Manejo de errores estandarizado

### Herramientas Disponibles
- `buscar_en_brave`: Búsqueda web usando Brave Search
- `generar_markdown`: Generación de contenido en formato Markdown
- `analizar_texto`: Análisis de texto usando Claude

### Recursos Disponibles
- `filesystem`: Operaciones de sistema de archivos
- `claude`: Operaciones con la API de Claude
- `search`: Operaciones de búsqueda
- `cache`: Operaciones de caché

## Control de Versiones

### Versiones
- v0.1.0 (Alpha) - Versión inicial con funcionalidades básicas
- v1.0.0 (Beta) - Implementación completa del protocolo MCP
- v1.1.0 (Beta) - Mejoras de rendimiento y seguridad
- v1.2.0 (Planned) - Mejoras de seguridad y rendimiento
- v1.3.0 (Planned) - Documentación completa y pruebas
- v2.0.0 (Planned) - Versión estable para producción

### Ramas
- `main` - Rama principal, código estable
- `develop` - Rama de desarrollo, características en progreso
- `feature/*` - Ramas para nuevas características
- `bugfix/*` - Ramas para correcciones de errores
- `release/*` - Ramas para preparación de releases

## Solución de Problemas

### El servidor no responde
- Verificar que el servidor esté ejecutándose
- Comprobar que no haya otro servicio usando el puerto 8000
- Verificar los logs en `logs/app.log`
- Asegurarse de que el host está configurado como `127.0.0.1` en el archivo `.env`

### Claude Desktop no se conecta
- Verificar la configuración en `claude_desktop_config.json`
- Asegurarse de que la API_KEY coincida en ambos lados
- Usar `127.0.0.1` en lugar de `localhost`
- Reiniciar Claude Desktop después de cambios en la configuración

### No se registran logs
- Verificar que el directorio `logs` existe y tiene permisos de escritura
- Comprobar que `LOG_LEVEL` está configurado correctamente en `.env`
- Asegurarse de que el servidor se inicia con `python -m app.main`

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

- GitHub Issues: [Reportar un problema](https://github.com/hectorflores28/mcp-claude/issues)
- Email: [tu-email@ejemplo.com]
