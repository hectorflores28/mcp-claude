# MCP-Claude

Sistema de integración con Claude 3.5 Sonnet para Claude Desktop.

## Estado Actual

### Implementado
- ✅ Estructura base del proyecto
- ✅ Configuración de FastAPI
- ✅ Sistema de logs estandarizado
- ✅ Integración con API de Claude
- ✅ Endpoints para Claude Desktop MCP
- ✅ Sistema de archivos
- ✅ Autenticación con API Key
- ✅ Endpoint de estado MCP mejorado
- ✅ Sistema de logging optimizado

### En Progreso
- 🔄 Mejora de la integración con Claude Desktop
- 🔄 Optimización del sistema de logs
- 🔄 Documentación de API

### Pendiente
- ⏳ Pruebas de integración
- ⏳ Pruebas de rendimiento
- ⏳ Despliegue en producción

## Requisitos

- Python 3.10+
- API Key de Claude
- Claude Desktop

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
│   │       └── ...
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── services/
│   │   ├── claude_service.py
│   │   └── ...
│   └── main.py
├── data/
├── logs/
├── temp/
├── uploads/
├── .env
└── requirements.txt
```

## Endpoints Principales

- `/api/health` - Estado del servidor
- `/api/mcp/status` - Estado para integración con Claude Desktop
- `/api/claude/status` - Estado del servicio de Claude
- `/api/claude/mcp/completion` - Endpoint para completado de Claude

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

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
