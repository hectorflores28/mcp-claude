# Ejemplos de Uso - MCP Claude

## 1. Búsqueda y Análisis de Información

### Ejemplo: Investigación de Tema

```python
import requests
import json

# Configuración
API_KEY = "tu_api_key"
BASE_URL = "http://localhost:8000/api/v1"

# 1. Realizar búsqueda
search_request = {
    "jsonrpc": "2.0",
    "method": "execute_tool",
    "params": {
        "tool_name": "buscar_en_brave",
        "parameters": {
            "query": "tendencias en inteligencia artificial 2024",
            "num_results": 5
        }
    },
    "id": 1
}

search_response = requests.post(
    f"{BASE_URL}/search",
    headers={"X-API-Key": API_KEY},
    json=search_request
)

# 2. Analizar resultados
analysis_request = {
    "jsonrpc": "2.0",
    "method": "execute_tool",
    "params": {
        "tool_name": "claude_analyze",
        "parameters": {
            "text": search_response.json()["result"]["result"]["results"][0]["description"],
            "analysis_type": "summary",
            "model": "claude-3-sonnet"
        }
    },
    "id": 2
}

analysis_response = requests.post(
    f"{BASE_URL}/claude/analyze",
    headers={"X-API-Key": API_KEY},
    json=analysis_request
)

print("Resumen del análisis:", analysis_response.json()["result"]["result"]["summary"])
```

## 2. Generación de Contenido

### Ejemplo: Creación de Artículo

```python
# 1. Generar estructura
structure_request = {
    "jsonrpc": "2.0",
    "method": "execute_tool",
    "params": {
        "tool_name": "claude_generate",
        "parameters": {
            "prompt": "Genera una estructura de artículo sobre las ventajas de la IA en la medicina",
            "max_tokens": 200,
            "temperature": 0.7,
            "model": "claude-3-opus"
        }
    },
    "id": 1
}

structure_response = requests.post(
    f"{BASE_URL}/claude/generate",
    headers={"X-API-Key": API_KEY},
    json=structure_request
)

# 2. Expandir cada sección
sections = structure_response.json()["result"]["result"]["text"].split("\n")
for section in sections:
    content_request = {
        "jsonrpc": "2.0",
        "method": "execute_tool",
        "params": {
            "tool_name": "claude_generate",
            "parameters": {
                "prompt": f"Expande esta sección del artículo: {section}",
                "max_tokens": 500,
                "temperature": 0.7,
                "model": "claude-3-opus"
            }
        },
        "id": 2
    }
    
    content_response = requests.post(
        f"{BASE_URL}/claude/generate",
        headers={"X-API-Key": API_KEY},
        json=content_request
    )
    
    print(f"Contenido de la sección: {content_response.json()['result']['result']['text']}")
```

## 3. Análisis de Sentimiento

### Ejemplo: Análisis de Reseñas

```python
# Lista de reseñas
reviews = [
    "Excelente servicio, muy rápido y eficiente",
    "El producto llegó dañado y el servicio al cliente fue pésimo",
    "Buen precio pero la calidad podría ser mejor"
]

for review in reviews:
# Añadir mensajes
conversation.add_message("Hola, ¿podrías ayudarme con un problema de programación?")
conversation.add_message("Estoy teniendo problemas con el manejo de errores en Python.")

# Obtener respuesta
response = conversation.get_response()
print(response.text)
```

### 3. Análisis de Texto

```python
# Analizar un documento largo
with open("documento.txt", "r") as f:
    text = f.read()

analysis = client.analyze_text(
    text=text,
    task="summarize",
    max_tokens=500
)
print(analysis.summary)
```

### 4. Uso del Sistema de Caché

```python
# La caché se activa automáticamente para respuestas idénticas
response1 = client.generate("¿Cuál es la capital de Francia?")
response2 = client.generate("¿Cuál es la capital de Francia?")  # Usará caché

# Invalidar caché para una consulta específica
client.invalidate_cache("¿Cuál es la capital de Francia?")
```

### 5. Monitoreo de Métricas

```python
# Las métricas se recopilan automáticamente
# Puedes acceder a ellas a través de Prometheus

# Ver métricas actuales
metrics = client.get_metrics()
print(f"Total de solicitudes: {metrics.requests_total}")
print(f"Tokens utilizados: {metrics.tokens_total}")
```

### 6. Manejo de Errores

```python
from mcp_claude.exceptions import ClaudeAPIError

try:
    response = client.generate("Genera un texto muy largo" * 1000)
except ClaudeAPIError as e:
    print(f"Error: {e.message}")
    print(f"Código: {e.code}")
    print(f"Detalles: {e.details}")
```

### 7. Uso Avanzado con Parámetros

```python
response = client.generate(
    prompt="Escribe un poema sobre la naturaleza",
    model="claude-3-opus",
    temperature=0.8,
    max_tokens=300,
    stop_sequences=["\n\n"],
    top_p=0.9,
    frequency_penalty=0.5,
    presence_penalty=0.5
)
```

### 8. Procesamiento por Lotes

```python
prompts = [
    "Resume este texto: ...",
    "Traduce esto al inglés: ...",
    "Analiza este código: ..."
]

responses = client.generate_batch(prompts)
for prompt, response in zip(prompts, responses):
    print(f"Prompt: {prompt[:50]}...")
    print(f"Respuesta: {response.text[:100]}...")
    print("---")
```

## Casos de Uso Avanzados

### Asistente de Programación

```python
# Crear un asistente especializado en programación
assistant = client.create_assistant(
    name="CodeHelper",
    instructions="Eres un experto en Python, especializado en debugging y optimización."
)

# Usar el asistente
response = assistant.help(
    "Tengo un error en este código: [código]",
    context="Estoy trabajando en un proyecto de procesamiento de datos."
)
```

### Análisis de Sentimientos

```python
# Analizar sentimientos en textos
sentiment = client.analyze_sentiment(
    text="Me encanta este producto, es excelente!",
    detailed=True
)
print(f"Sentimiento: {sentiment.score}")
print(f"Confianza: {sentiment.confidence}")
print(f"Detalles: {sentiment.details}")
```

## Mejores Prácticas

1. **Gestión de API Keys**: Usa variables de entorno para las API keys
2. **Manejo de Errores**: Implementa siempre bloques try/except
3. **Optimización de Caché**: Usa la caché para consultas frecuentes
4. **Monitoreo**: Revisa regularmente las métricas de uso
5. **Límites de Tasa**: Implementa backoff exponencial para errores de límite de tasa 