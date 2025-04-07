# Integración con Claude Desktop

## Introducción

Esta guía proporciona instrucciones detalladas para integrar el servidor MCP-Claude con Claude Desktop. El servidor MCP-Claude implementa el protocolo MCP (Model Context Protocol) que permite a Claude Desktop interactuar con recursos externos y realizar operaciones avanzadas.

## Requisitos Previos

- Python 3.10+
- Redis 6.0+
- Claude Desktop v1.1.0 o superior
- Acceso a la API de Claude

## Configuración del Servidor MCP

### 1. Instalación

```bash
# Clonar repositorio
git clone https://github.com/hectorflores28/mcp-claude.git
cd mcp-claude

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración de Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
# Asegúrate de configurar:
# - API_KEY
# - CLAUDE_API_KEY
# - REDIS_HOST, REDIS_PORT, etc.
```

### 3. Iniciar Servicios

```bash
# Iniciar Redis
redis-server

# Iniciar servidor MCP
uvicorn app.main:app --reload --log-level debug
```

## Configuración de Claude Desktop

### 1. Crear Archivo de Configuración

Crea un archivo `claude_desktop_config.json` con el siguiente contenido:

```json
{
  "mcp_endpoint": "http://localhost:8000/api/mcp",
  "api_key": "tu-clave-secreta",
  "cache_enabled": true,
  "retry_policy": {
    "max_attempts": 3,
    "delay": 1.5
  }
}
```

### 2. Copiar Configuración

- Copia el archivo `claude_desktop_config.json` a la carpeta de configuración de Claude Desktop
- La ubicación exacta depende de tu sistema operativo:
  - Windows: `%APPDATA%\Claude Desktop\config\`
  - macOS: `~/Library/Application Support/Claude Desktop/config/`
  - Linux: `~/.config/claude-desktop/`

### 3. Reiniciar Claude Desktop

- Cierra Claude Desktop completamente
- Vuelve a abrir Claude Desktop
- El protocolo MCP estará disponible automáticamente

## Verificación de la Integración

### 1. Verificar Estado del Servidor

```bash
# Verificar que el servidor MCP está funcionando
curl http://localhost:8000/health

# Verificar estado del protocolo MCP
curl http://localhost:8000/api/mcp/status
```

### 2. Ejecutar Pruebas de Integración

```bash
# Ejecutar suite de pruebas de integración
pytest tests/integration/test_mcp_connection.py -v
```

### 3. Verificar Logs

```bash
# Verificar logs del servidor MCP
tail -f logs/mcp.log
```

## Uso del Protocolo MCP en Claude Desktop

### 1. Operaciones Básicas

Claude Desktop puede utilizar el protocolo MCP para realizar las siguientes operaciones:

- **Búsqueda de información**: Buscar información en la web
- **Operaciones de archivos**: Leer, escribir y manipular archivos
- **Acceso a recursos**: Acceder a recursos externos
- **Ejecución de herramientas**: Ejecutar herramientas externas

### 2. Ejemplo de Uso

Cuando Claude Desktop necesita realizar una operación que requiere el protocolo MCP, automáticamente enviará una solicitud al servidor MCP. Por ejemplo:

```json
{
  "operation": "search",
  "parameters": {
    "query": "información sobre inteligencia artificial",
    "max_results": 5
  }
}
```

El servidor MCP procesará la solicitud y devolverá una respuesta:

```json
{
  "status": "success",
  "result": {
    "results": [
      {
        "title": "Inteligencia Artificial - Wikipedia",
        "url": "https://es.wikipedia.org/wiki/Inteligencia_artificial",
        "snippet": "La inteligencia artificial (IA) es la inteligencia llevada a cabo por máquinas..."
      },
      // ... más resultados
    ]
  }
}
```

### 3. Operaciones Disponibles

El servidor MCP-Claude soporta las siguientes operaciones:

| Operación | Descripción | Parámetros |
|-----------|-------------|------------|
| `search` | Búsqueda en la web | `query`, `max_results`, `country`, `language` |
| `read_file` | Leer archivo | `path`, `encoding` |
| `write_file` | Escribir archivo | `path`, `content`, `encoding` |
| `list_files` | Listar archivos | `path`, `pattern`, `recursive` |
| `delete_file` | Eliminar archivo | `path` |
| `get_resource` | Obtener recurso | `resource_id`, `parameters` |
| `execute_tool` | Ejecutar herramienta | `tool_id`, `parameters` |

## Solución de Problemas

### Problemas Comunes

#### ⚠️ Claude Desktop no se conecta al servidor MCP

**Solución**:
1. Verifica que el servidor MCP está en ejecución
2. Comprueba que la URL en `claude_desktop_config.json` es correcta
3. Verifica que no hay firewalls bloqueando la conexión

#### ⚠️ Errores de autenticación

**Solución**:
1. Verifica que la API Key en `claude_desktop_config.json` coincide con la del servidor MCP
2. Comprueba que la API Key en `.env` es correcta
3. Regenera una nueva API Key si es necesario

#### ⚠️ Operaciones MCP fallan

**Solución**:
1. Verifica los logs del servidor MCP
2. Comprueba que los parámetros de la operación son correctos
3. Ejecuta las pruebas de integración para identificar el problema

## Recursos Adicionales

- [Documentación de la API MCP](https://github.com/hectorflores28/mcp-claude/blob/main/docs/api.md)
- [Guía de Solución de Problemas](https://github.com/hectorflores28/mcp-claude/blob/main/docs/troubleshooting.md)
- [Lista de Verificación de Integración](https://github.com/hectorflores28/mcp-claude/blob/main/docs/integration_checklist.md)
- [Ejemplos de Código](https://github.com/hectorflores28/mcp-claude/blob/main/examples/) 