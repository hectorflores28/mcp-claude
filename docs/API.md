# Documentación de la API MCP Claude

## Introducción

Esta API implementa el protocolo MCP (Model Context Protocol) para interactuar con herramientas externas como Brave Search y Claude, además de proporcionar operaciones en el sistema de archivos.

## Endpoints

### 1. Búsqueda con Brave Search

**Endpoint:** `POST /api/v1/search`

**Descripción:** Realiza una búsqueda utilizando la API de Brave Search.

**Ejemplo de solicitud:**
```json
{
  "jsonrpc": "2.0",
  "method": "execute_tool",
  "params": {
    "tool_name": "buscar_en_brave",
    "parameters": {
      "query": "últimas noticias de IA",
      "num_results": 5
    }
  },
  "id": 1
}
```

**Ejemplo de respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tool_name": "buscar_en_brave",
    "parameters": {
      "query": "últimas noticias de IA",
      "num_results": 5
    },
    "result": {
      "results": [
        {
          "title": "Título del resultado",
          "url": "https://ejemplo.com",
          "description": "Descripción del resultado",
          "source": "brave_search"
        }
      ],
      "total_results": 1,
      "query": "últimas noticias de IA"
    }
  },
  "id": 1
}
```

### 2. Operaciones en Sistema de Archivos

**Endpoint:** `POST /api/v1/filesystem`

**Descripción:** Realiza operaciones CRUD en archivos Markdown.

**Ejemplo de solicitud:**
```json
{
  "jsonrpc": "2.0",
  "method": "execute_tool",
  "params": {
    "tool_name": "filesystem_operation",
    "parameters": {
      "operation": "create",
      "path": "ejemplo.md",
      "content": "# Título\n\nContenido del archivo"
    }
  },
  "id": 1
}
```

**Ejemplo de respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tool_name": "filesystem_operation",
    "parameters": {
      "operation": "create",
      "path": "ejemplo.md"
    },
    "result": {
      "success": true,
      "message": "Archivo creado exitosamente",
      "path": "/app/data/ejemplo.md"
    }
  },
  "id": 1
}
```

### 3. Generación de Texto con Claude

**Endpoint:** `POST /api/v1/claude/generate`

**Descripción:** Genera texto utilizando el modelo Claude.

**Ejemplo de solicitud:**
```json
{
  "jsonrpc": "2.0",
  "method": "execute_tool",
  "params": {
    "tool_name": "claude_generate",
    "parameters": {
      "prompt": "Escribe un párrafo sobre la inteligencia artificial",
      "max_tokens": 100,
      "temperature": 0.7,
      "model": "claude-3-opus"
    }
  },
  "id": 1
}
```

**Ejemplo de respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tool_name": "claude_generate",
    "parameters": {
      "prompt": "Escribe un párrafo sobre la inteligencia artificial",
      "max_tokens": 100,
      "temperature": 0.7,
      "model": "claude-3-opus"
    },
    "result": {
      "text": "La inteligencia artificial (IA) representa una revolución tecnológica que está transformando prácticamente todos los aspectos de nuestra vida cotidiana. Desde asistentes virtuales que responden a nuestras preguntas hasta sistemas de recomendación que personalizan nuestra experiencia en línea, la IA está cada vez más presente en nuestro día a día. Los avances en aprendizaje automático y procesamiento del lenguaje natural han permitido que las máquinas comprendan y generen lenguaje humano con una precisión sin precedentes, abriendo nuevas posibilidades para la automatización de tareas complejas y la creación de experiencias interactivas más naturales.",
      "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 85,
        "total_tokens": 100
      }
    }
  },
  "id": 1
}
```

### 4. Análisis de Texto con Claude

**Endpoint:** `POST /api/v1/claude/analyze`

**Descripción:** Analiza texto utilizando el modelo Claude.

**Ejemplo de solicitud:**
```json
{
  "jsonrpc": "2.0",
  "method": "execute_tool",
  "params": {
    "tool_name": "claude_analyze",
    "parameters": {
      "text": "Este producto es excelente, me encanta su calidad y servicio al cliente.",
      "analysis_type": "sentiment",
      "model": "claude-3-sonnet"
    }
  },
  "id": 1
}
```

**Ejemplo de respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tool_name": "claude_analyze",
    "parameters": {
      "text": "Este producto es excelente, me encanta su calidad y servicio al cliente.",
      "analysis_type": "sentiment",
      "model": "claude-3-sonnet"
    },
    "result": {
      "sentiment": "POSITIVE",
      "confidence": 0.95,
      "details": {
        "emotions": ["satisfaction", "enthusiasm"],
        "aspects": ["product quality", "customer service"]
      }
    }
  },
  "id": 1
}
```

### 5. Ejecución de Herramientas

**Endpoint:** `POST /api/v1/execute`

**Descripción:** Endpoint principal para ejecutar cualquier herramienta MCP.

**Ejemplo de solicitud:**
```json
{
  "jsonrpc": "2.0",
  "method": "execute_tool",
  "params": {
    "tool_name": "generate_summary",
    "parameters": {
      "content": "Texto a resumir"
    }
  },
  "id": 1
}
```

## Autenticación

La API utiliza autenticación mediante API keys. Incluye tu API key en el header `X-API-Key` de cada solicitud.

## Códigos de Error

- `400`: Solicitud mal formada
- `401`: No autorizado
- `403`: Prohibido
- `404`: Recurso no encontrado
- `500`: Error interno del servidor

## Formato de Error

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": 500,
    "message": "Descripción del error",
    "data": {
      "detalles": "Información adicional"
    }
  },
  "id": 1
}
``` 