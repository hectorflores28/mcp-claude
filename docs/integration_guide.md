# Guía de Integración con Claude Desktop

## Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración del Servidor MCP](#configuración-del-servidor-mcp)
3. [Configuración de Claude Desktop](#configuración-de-claude-desktop)
4. [Pruebas de Integración](#pruebas-de-integración)
5. [Solución de Problemas](#solución-de-problemas)
6. [Flujos de Trabajo Recomendados](#flujos-de-trabajo-recomendados)

## Requisitos Previos

- Python 3.10+
- Redis 6.0+
- Claude Desktop v1.1.0 o superior
- Acceso a la API de Claude

## Configuración del Servidor MCP

1. **Instalación del Servidor**:
   ```bash
   git clone https://github.com/hectorflores28/mcp-claude.git
   cd mcp-claude
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

2. **Configuración de Variables de Entorno**:
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

3. **Iniciar Servicios**:
   ```bash
   # Iniciar Redis
   redis-server
   
   # Iniciar servidor MCP
   uvicorn app.main:app --reload --log-level debug
   ```

## Configuración de Claude Desktop

1. **Crear Archivo de Configuración**:
   ```bash
   # Crear archivo claude_desktop_config.json
   echo '{
     "mcp_endpoint": "http://localhost:8000/api/mcp",
     "api_key": "tu-clave-secreta",
     "cache_enabled": true,
     "retry_policy": {
       "max_attempts": 3,
       "delay": 1.5
     }
   }' > claude_desktop_config.json
   ```

2. **Copiar Configuración**:
   - Copiar `claude_desktop_config.json` a la carpeta de configuración de Claude Desktop
   - Reiniciar Claude Desktop

## Pruebas de Integración

### Checklist de Pruebas Iniciales

- [ ] Test de conexión básica
- [ ] Autenticación con API Key
- [ ] Operación MCP básica (GET /status)
- [ ] Ejecución simple de prompt
- [ ] Validación de formatos de respuesta
- [ ] Prueba de sistema de caché
- [ ] Verificación de logs

### Ejecutar Pruebas

```bash
# Ejecutar suite de pruebas de integración
pytest tests/integration/test_mcp_connection.py -v

# Generar reporte de cobertura
pytest --cov=app --cov-report=html
```

## Solución de Problemas

### Problemas Comunes

#### ⚠️ Timeout en conexión
**Solución**: 
- Verificar firewall y puertos (8000 para MCP, 6379 para Redis)
- Comprobar que Redis está ejecutándose: `redis-cli ping`
- Verificar que el servidor MCP está activo: `curl -I http://localhost:8000/docs`

#### ⚠️ Errores de autenticación
**Solución**:
1. Verificar que la API Key en `.env` coincide con la configuración de Claude Desktop
2. Comprobar encabezados HTTP correctos: `Authorization: Bearer <token>`
3. Verificar que los tokens JWT no han expirado

#### ⚠️ Errores de serialización
**Solución**:
- Validar formatos con:
  ```bash
  curl -X POST http://localhost:8000/api/mcp/execute \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <token>" \
    -d '{"operation": "test"}'
  ```

## Flujos de Trabajo Recomendados

### Flujo Básico de Integración

1. **Iniciar Servidor MCP**:
   ```bash
   uvicorn app.main:app --reload --log-level debug
   ```

2. **Verificar Servicios**:
   ```bash
   # Verificar Redis
   redis-cli ping  # Debe responder PONG
   
   # Verificar API
   curl -I http://localhost:8000/docs  # Debe dar 200 OK
   ```

3. **Ejecutar Pruebas de Integración**:
   ```bash
   pytest tests/integration/test_mcp_connection.py -v
   ```

4. **Monitorear Logs**:
   ```bash
   tail -f logs/mcp.log
   ```

### Ejemplo de Código para Claude Desktop

```python
# Ejemplo de conexión inicial
from mcp_integration import ClaudeMCPClient

client = ClaudeMCPClient(
    endpoint="http://localhost:8000/api/mcp",
    api_key="tu-clave-secreta"
)

# Verificar estado
status = client.get_mcp_status()
print(f"Estado MCP: {status.version} - {status.status}")

# Ejecutar operación
result = client.execute_operation(
    operation="test",
    parameters={}
)
print(f"Resultado: {result}")
``` 