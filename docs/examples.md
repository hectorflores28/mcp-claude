# Ejemplos de Uso de MCP-Claude

## Instalación

```bash
pip install mcp-claude
```

## Configuración Básica

```python
from mcp_claude import ClaudeClient

# Inicializar el cliente
client = ClaudeClient(api_key="tu-api-key")

# Configurar opciones globales
client.set_default_model("claude-3-opus")
client.set_default_temperature(0.7)
```

## Ejemplos de Uso

### 1. Generación de Texto Simple

```python
# Generar una respuesta simple
response = client.generate(
    prompt="Explica el concepto de inteligencia artificial en tres párrafos."
)
print(response.text)
```

### 2. Conversación con Contexto

```python
# Iniciar una conversación
conversation = client.start_conversation()

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