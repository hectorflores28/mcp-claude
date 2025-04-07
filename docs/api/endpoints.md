# Endpoints de MCP-Claude

## Endpoints de Claude

### Generación de Texto
```http
POST /api/v1/claude/generate
```

Genera texto utilizando el modelo Claude.

#### Parámetros
- `prompt` (string, requerido): El texto de entrada para la generación
- `max_tokens` (integer, opcional): Número máximo de tokens a generar
- `temperature` (float, opcional): Control de aleatoriedad (0.0 a 1.0)

#### Respuesta
```json
{
    "text": "Texto generado por Claude",
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 50,
        "total_tokens": 60
    }
}
```

### Análisis de Texto
```http
POST /api/v1/claude/analyze
```

Analiza texto utilizando el modelo Claude.

#### Parámetros
- `text` (string, requerido): El texto a analizar
- `analysis_type` (string, requerido): Tipo de análisis a realizar

#### Respuesta
```json
{
    "analysis": {
        "sentiment": "positive",
        "confidence": 0.95,
        "details": {}
    }
}
```

## Endpoints de Búsqueda

### Búsqueda Web
```http
GET /api/v1/search
```

Realiza una búsqueda web utilizando Brave Search.

#### Parámetros
- `query` (string, requerido): Términos de búsqueda
- `limit` (integer, opcional): Número máximo de resultados

#### Respuesta
```json
{
    "results": [
        {
            "title": "Título del resultado",
            "url": "https://ejemplo.com",
            "snippet": "Descripción del resultado"
        }
    ]
}
```

## Endpoints del Sistema de Archivos

### Operaciones de Archivos
```http
POST /api/v1/filesystem/operation
```

Realiza operaciones en el sistema de archivos.

#### Parámetros
- `operation` (string, requerido): Tipo de operación
- `path` (string, requerido): Ruta del archivo
- `content` (string, opcional): Contenido para escritura

#### Respuesta
```json
{
    "success": true,
    "operation": "read",
    "result": {}
}
``` 