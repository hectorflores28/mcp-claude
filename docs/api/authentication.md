# Autenticación en MCP-Claude

## Configuración de API Keys

MCP-Claude requiere dos API keys principales:

1. **Claude API Key**
   - Obtenida de Anthropic
   - Configurada en `CLAUDE_API_KEY`

2. **Brave Search API Key**
   - Obtenida de Brave Search
   - Configurada en `BRAVE_SEARCH_API_KEY`

## Autenticación en Endpoints

Todos los endpoints requieren autenticación mediante API key en el header:

```http
Authorization: Bearer <api_key>
```

### Headers Requeridos

```http
Content-Type: application/json
Authorization: Bearer <api_key>
```

## Manejo de API Keys

### Configuración en .env
```env
CLAUDE_API_KEY=your_claude_api_key
BRAVE_SEARCH_API_KEY=your_brave_search_api_key
```

### Rotación de API Keys

Se recomienda rotar las API keys periódicamente:

1. Generar nueva API key
2. Actualizar en el archivo .env
3. Actualizar en el sistema de despliegue
4. Mantener la key anterior por 24 horas antes de revocarla

## Seguridad

### Mejores Prácticas

1. Nunca compartir API keys en código
2. Usar variables de entorno
3. Implementar rate limiting
4. Monitorear uso de API keys
5. Rotar keys periódicamente

### Rate Limiting

Los límites de rate son:

- Claude API: 100 requests/minuto
- Brave Search: 1000 requests/día

## Ejemplos

### Python
```python
import requests

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

response = requests.post(
    'http://localhost:8000/api/v1/claude/generate',
    headers=headers,
    json={'prompt': 'Hello, Claude!'}
)
```

### cURL
```bash
curl -X POST \
  http://localhost:8000/api/v1/claude/generate \
  -H 'Authorization: Bearer your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Hello, Claude!"}'
``` 