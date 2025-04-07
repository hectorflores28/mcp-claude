# Manejo de Errores en MCP-Claude

## Códigos de Error

### Errores de Claude API

| Código | Descripción |
|--------|-------------|
| `CLAUDE_API_ERROR` | Error general de la API de Claude |
| `CLAUDE_RATE_LIMIT` | Se ha excedido el límite de rate |
| `CLAUDE_TOKEN_LIMIT` | Se ha excedido el límite de tokens |
| `CLAUDE_CONTENT_FILTER` | El contenido ha sido filtrado |

### Errores de Búsqueda

| Código | Descripción |
|--------|-------------|
| `SEARCH_API_ERROR` | Error general de la API de búsqueda |
| `SEARCH_RATE_LIMIT` | Se ha excedido el límite de búsquedas |
| `SEARCH_INVALID_QUERY` | Query de búsqueda inválida |

### Errores de Sistema de Archivos

| Código | Descripción |
|--------|-------------|
| `FILE_NOT_FOUND` | Archivo no encontrado |
| `FILE_PERMISSION_DENIED` | Permisos insuficientes |
| `FILE_OPERATION_FAILED` | Error en operación de archivo |

### Errores de Autenticación

| Código | Descripción |
|--------|-------------|
| `AUTH_INVALID_KEY` | API key inválida |
| `AUTH_EXPIRED_KEY` | API key expirada |
| `AUTH_MISSING_KEY` | API key no proporcionada |

## Formato de Respuesta de Error

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Descripción del error",
        "details": {
            "field": "Información adicional"
        }
    }
}
```

## Ejemplos de Errores

### Error de Rate Limit
```json
{
    "error": {
        "code": "CLAUDE_RATE_LIMIT",
        "message": "Se ha excedido el límite de requests por minuto",
        "details": {
            "retry_after": 60
        }
    }
}
```

### Error de Autenticación
```json
{
    "error": {
        "code": "AUTH_INVALID_KEY",
        "message": "API key inválida o expirada",
        "details": {
            "key_type": "claude"
        }
    }
}
```

## Manejo de Errores

### Python
```python
try:
    response = client.generate_text(prompt="Hello")
except ClaudeAPIError as e:
    if e.code == "CLAUDE_RATE_LIMIT":
        time.sleep(e.details["retry_after"])
        # Reintentar la operación
    else:
        # Manejar otros errores
```

### Mejores Prácticas

1. Siempre verificar el código de error
2. Implementar reintentos para errores temporales
3. Registrar errores para debugging
4. Proporcionar mensajes de error útiles
5. Manejar errores de forma segura 