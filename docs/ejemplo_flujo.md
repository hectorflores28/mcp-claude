# Ejemplo de Flujo de Trabajo con MCP Claude

## Escenario: Análisis y Generación de Contenido

Este ejemplo muestra un flujo de trabajo completo utilizando MCP Claude para realizar búsquedas, análisis y generación de contenido.

### 1. Búsqueda de Información

```python
import requests

# Realizar búsqueda
search_response = requests.post(
    "http://localhost:8000/api/v1/search",
    headers={"X-API-Key": "tu-api-key"},
    json={
        "jsonrpc": "2.0",
        "method": "execute_tool",
        "params": {
            "tool_name": "brave_search",
            "parameters": {
                "query": "tendencias en inteligencia artificial 2024",
                "count": 5
            }
        },
        "id": 1
    }
)

search_results = search_response.json()["result"]["result"]["results"]
```

### 2. Análisis de Resultados

```python
# Analizar el primer resultado
analysis_response = requests.post(
    "http://localhost:8000/api/v1/claude/analyze",
    headers={"X-API-Key": "tu-api-key"},
    json={
        "jsonrpc": "2.0",
        "method": "execute_tool",
        "params": {
            "tool_name": "claude_analyze",
            "parameters": {
                "text": search_results[0]["description"],
                "analysis_type": "summary",
                "model": "claude-3-opus"
            }
        },
        "id": 2
    }
)

analysis = analysis_response.json()["result"]["result"]
```

### 3. Generación de Contenido

```python
# Generar artículo basado en el análisis
generate_response = requests.post(
    "http://localhost:8000/api/v1/claude/generate",
    headers={"X-API-Key": "tu-api-key"},
    json={
        "jsonrpc": "2.0",
        "method": "execute_tool",
        "params": {
            "tool_name": "claude_generate",
            "parameters": {
                "prompt": f"Escribe un artículo sobre {analysis['summary']}",
                "model": "claude-3-opus",
                "max_tokens": 1000
            }
        },
        "id": 3
    }
)

article = generate_response.json()["result"]["result"]["text"]
```

### 4. Guardar el Resultado

```python
# Guardar el artículo
save_response = requests.post(
    "http://localhost:8000/api/v1/filesystem",
    headers={"X-API-Key": "tu-api-key"},
    json={
        "jsonrpc": "2.0",
        "method": "execute_tool",
        "params": {
            "tool_name": "filesystem_operation",
            "parameters": {
                "operation": "write",
                "path": "articulos/ia_tendencias_2024.md",
                "content": article
            }
        },
        "id": 4
    }
)
```

## Escenario: Análisis de Sentimiento en Tiempo Real

Este ejemplo muestra cómo realizar un análisis de sentimiento en tiempo real sobre un flujo de datos.

### 1. Configuración del Procesamiento en Lote

```python
def process_reviews(reviews):
    results = []
    for review in reviews:
        response = requests.post(
            "http://localhost:8000/api/v1/claude/analyze",
            headers={"X-API-Key": "tu-api-key"},
            json={
                "jsonrpc": "2.0",
                "method": "execute_tool",
                "params": {
                    "tool_name": "claude_analyze",
                    "parameters": {
                        "text": review,
                        "analysis_type": "sentiment",
                        "model": "claude-3-opus"
                    }
                },
                "id": 1
            }
        )
        results.append(response.json()["result"]["result"])
    return results
```

### 2. Procesamiento de Datos en Tiempo Real

```python
def real_time_analysis(text_stream):
    for text in text_stream:
        response = requests.post(
            "http://localhost:8000/api/v1/claude/analyze",
            headers={"X-API-Key": "tu-api-key"},
            json={
                "jsonrpc": "2.0",
                "method": "execute_tool",
                "params": {
                    "tool_name": "claude_analyze",
                    "parameters": {
                        "text": text,
                        "analysis_type": "sentiment",
                        "model": "claude-3-opus"
                    }
                },
                "id": 1
            }
        )
        yield response.json()["result"]["result"]
```

## Escenario: Pipeline de Procesamiento de Documentos

Este ejemplo muestra cómo crear un pipeline completo para procesar documentos.

### 1. Pipeline de Procesamiento

```python
def document_pipeline(document_path):
    # 1. Leer documento
    read_response = requests.post(
        "http://localhost:8000/api/v1/filesystem",
        headers={"X-API-Key": "tu-api-key"},
        json={
            "jsonrpc": "2.0",
            "method": "execute_tool",
            "params": {
                "tool_name": "filesystem_operation",
                "parameters": {
                    "operation": "read",
                    "path": document_path
                }
            },
            "id": 1
        }
    )
    content = read_response.json()["result"]["result"]["content"]

    # 2. Analizar contenido
    analysis_response = requests.post(
        "http://localhost:8000/api/v1/claude/analyze",
        headers={"X-API-Key": "tu-api-key"},
        json={
            "jsonrpc": "2.0",
            "method": "execute_tool",
            "params": {
                "tool_name": "claude_analyze",
                "parameters": {
                    "text": content,
                    "analysis_type": "summary",
                    "model": "claude-3-opus"
                }
            },
            "id": 2
        }
    )
    analysis = analysis_response.json()["result"]["result"]

    # 3. Generar recomendaciones
    generate_response = requests.post(
        "http://localhost:8000/api/v1/claude/generate",
        headers={"X-API-Key": "tu-api-key"},
        json={
            "jsonrpc": "2.0",
            "method": "execute_tool",
            "params": {
                "tool_name": "claude_generate",
                "parameters": {
                    "prompt": f"Basado en este análisis: {analysis['summary']}, genera recomendaciones",
                    "model": "claude-3-opus"
                }
            },
            "id": 3
        }
    )
    recommendations = generate_response.json()["result"]["result"]["text"]

    return {
        "content": content,
        "analysis": analysis,
        "recommendations": recommendations
    }
```

## Mejores Prácticas

1. **Manejo de Errores**
   - Implementar reintentos para llamadas a la API
   - Validar respuestas
   - Manejar timeouts

2. **Optimización**
   - Usar caché cuando sea posible
   - Implementar procesamiento por lotes
   - Monitorear uso de tokens

3. **Seguridad**
   - Rotar API keys regularmente
   - Validar entradas
   - Implementar rate limiting

4. **Monitoreo**
   - Registrar métricas importantes
   - Configurar alertas
   - Mantener logs detallados 