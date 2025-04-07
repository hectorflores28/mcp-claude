# Guía de Solución de Problemas para MCP-Claude

## Índice

1. [Problemas de Conexión](#problemas-de-conexión)
2. [Problemas de Autenticación](#problemas-de-autenticación)
3. [Problemas de Rendimiento](#problemas-de-rendimiento)
4. [Problemas de Caché](#problemas-de-caché)
5. [Problemas de Logs](#problemas-de-logs)
6. [Problemas de Integración con Claude Desktop](#problemas-de-integración-con-claude-desktop)

## Problemas de Conexión

### ⚠️ El servidor MCP no responde

**Síntomas**:
- Timeout al intentar conectar con el servidor
- Error "Connection refused" al intentar acceder a la API

**Solución**:
1. Verificar que el servidor está en ejecución:
   ```bash
   ps aux | grep uvicorn
   ```

2. Comprobar que el puerto 8000 está abierto:
   ```bash
   netstat -tuln | grep 8000
   ```

3. Verificar la configuración de firewall:
   ```bash
   # Windows
   netsh advfirewall firewall show rule name="MCP Server"
   
   # Linux
   sudo ufw status
   ```

4. Reiniciar el servidor con modo debug:
   ```bash
   uvicorn app.main:app --reload --log-level debug
   ```

### ⚠️ Redis no está disponible

**Síntomas**:
- Errores de conexión a Redis
- Mensajes de error relacionados con el caché

**Solución**:
1. Verificar que Redis está en ejecución:
   ```bash
   redis-cli ping
   ```

2. Comprobar la configuración de Redis en `.env`:
   ```
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   ```

3. Reiniciar Redis:
   ```bash
   # Windows
   net stop redis
   net start redis
   
   # Linux
   sudo systemctl restart redis
   ```

## Problemas de Autenticación

### ⚠️ API Key no válida

**Síntomas**:
- Error 401 Unauthorized
- Mensaje "Invalid API key"

**Solución**:
1. Verificar que la API Key en `.env` coincide con la configuración de Claude Desktop:
   ```
   API_KEY=tu-clave-secreta
   ```

2. Comprobar que la API Key está correctamente configurada en `claude_desktop_config.json`:
   ```json
   {
     "api_key": "tu-clave-secreta"
   }
   ```

3. Regenerar una nueva API Key si es necesario:
   ```bash
   # Generar una nueva API Key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### ⚠️ Token JWT expirado

**Síntomas**:
- Error 401 Unauthorized
- Mensaje "Token has expired"

**Solución**:
1. Verificar la configuración de expiración de tokens en `.env`:
   ```
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

2. Obtener un nuevo token:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/token \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'
   ```

3. Actualizar el token en la configuración de Claude Desktop

## Problemas de Rendimiento

### ⚠️ Respuestas lentas

**Síntomas**:
- Tiempos de respuesta superiores a 5 segundos
- Timeouts frecuentes

**Solución**:
1. Verificar la configuración de caché:
   ```
   CACHE_TTL=300
   CACHE_PREFIX=mcp:
   ```

2. Comprobar la configuración de Redis:
   ```
   REDIS_MAX_CONNECTIONS=10
   REDIS_TIMEOUT=5
   ```

3. Optimizar consultas a la base de datos:
   - Revisar índices
   - Optimizar consultas complejas
   - Implementar paginación

### ⚠️ Alto uso de CPU

**Síntomas**:
- CPU constantemente al 100%
- Respuestas lentas

**Solución**:
1. Verificar la configuración de workers:
   ```bash
   uvicorn app.main:app --workers 4
   ```

2. Implementar rate limiting:
   ```
   RATE_LIMIT_WINDOW=60
   RATE_LIMIT_MAX_REQUESTS=100
   ```

3. Optimizar operaciones costosas:
   - Implementar procesamiento asíncrono
   - Utilizar tareas en segundo plano
   - Optimizar algoritmos

## Problemas de Caché

### ⚠️ Caché no funciona

**Síntomas**:
- Respuestas lentas
- Carga constante en la base de datos

**Solución**:
1. Verificar la conexión a Redis:
   ```bash
   redis-cli ping
   ```

2. Comprobar la configuración de caché:
   ```
   CACHE_TTL=300
   CACHE_PREFIX=mcp:
   ```

3. Limpiar la caché:
   ```bash
   redis-cli FLUSHALL
   ```

### ⚠️ Datos obsoletos en caché

**Síntomas**:
- Información desactualizada
- Inconsistencias en los datos

**Solución**:
1. Verificar la configuración de TTL:
   ```
   CACHE_TTL=300
   ```

2. Implementar invalidación de caché:
   ```python
   # Ejemplo de invalidación de caché
   await cache.delete(f"{CACHE_PREFIX}status")
   ```

3. Utilizar versiones de caché:
   ```python
   # Ejemplo de versionado de caché
   cache_key = f"{CACHE_PREFIX}status:v1"
   ```

## Problemas de Logs

### ⚠️ Logs no se generan

**Síntomas**:
- No hay archivos de log
- Errores no registrados

**Solución**:
1. Verificar la configuración de logs:
   ```
   LOG_LEVEL=INFO
   LOG_DIR=logs
   LOG_MAX_BYTES=10485760
   LOG_BACKUP_COUNT=5
   ```

2. Comprobar permisos de directorio:
   ```bash
   # Windows
   icacls logs
   
   # Linux
   ls -la logs
   ```

3. Crear directorio de logs si no existe:
   ```bash
   mkdir -p logs
   ```

### ⚠️ Logs demasiado grandes

**Síntomas**:
- Archivos de log muy grandes
- Espacio en disco agotado

**Solución**:
1. Ajustar la rotación de logs:
   ```
   LOG_MAX_BYTES=10485760  # 10MB
   LOG_BACKUP_COUNT=5
   ```

2. Implementar limpieza automática:
   ```bash
   # Ejemplo de script de limpieza
   find logs -name "*.log" -mtime +7 -delete
   ```

3. Configurar logrotate:
   ```
   /path/to/logs/*.log {
       daily
       rotate 7
       compress
       delaycompress
       missingok
       notifempty
       create 0640 www-data www-data
   }
   ```

## Problemas de Integración con Claude Desktop

### ⚠️ Claude Desktop no se conecta

**Síntomas**:
- Claude Desktop muestra error de conexión
- No se establece comunicación con el servidor MCP

**Solución**:
1. Verificar la configuración en `claude_desktop_config.json`:
   ```json
   {
     "mcp_endpoint": "http://localhost:8000/api/mcp",
     "api_key": "tu-clave-secreta"
   }
   ```

2. Comprobar que el servidor MCP está accesible:
   ```bash
   curl -I http://localhost:8000/api/mcp/status
   ```

3. Verificar la configuración de red:
   - Asegurarse de que no hay firewalls bloqueando
   - Comprobar que los puertos están abiertos
   - Verificar que las URLs son accesibles

### ⚠️ Operaciones MCP fallan

**Síntomas**:
- Errores al ejecutar operaciones MCP
- Respuestas inesperadas

**Solución**:
1. Verificar el formato de las solicitudes:
   ```json
   {
     "operation": "test",
     "parameters": {}
   }
   ```

2. Comprobar los logs del servidor:
   ```bash
   tail -f logs/mcp.log
   ```

3. Ejecutar pruebas de integración:
   ```bash
   pytest tests/integration/test_mcp_connection.py -v
   ```

### ⚠️ Problemas de compatibilidad

**Síntomas**:
- Errores de versión
- Funcionalidades no disponibles

**Solución**:
1. Verificar la versión de Claude Desktop:
   - Asegurarse de que es v1.1.0 o superior

2. Comprobar la versión del servidor MCP:
   ```bash
   curl http://localhost:8000/api/mcp/status | jq .version
   ```

3. Actualizar a la última versión si es necesario:
   ```bash
   git pull
   pip install -r requirements.txt
   ``` 