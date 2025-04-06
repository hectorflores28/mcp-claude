from anthropic import Anthropic
from typing import Dict, List, Optional
from app.core.config import settings

class ClaudeService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Genera una respuesta usando Claude.
        
        Args:
            prompt: El prompt principal
            system_prompt: Prompt del sistema (opcional)
            max_tokens: Máximo de tokens a generar (opcional)
            
        Returns:
            Respuesta generada por Claude
        """
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
    
    async def analyze_search_results(
        self,
        query: str,
        results: List[Dict]
    ) -> str:
        """
        Analiza los resultados de búsqueda usando Claude.
        
        Args:
            query: Término de búsqueda original
            results: Lista de resultados de búsqueda
            
        Returns:
            Análisis de los resultados
        """
        system_prompt = """Eres un asistente experto en análisis de información.
        Tu tarea es analizar los resultados de búsqueda y proporcionar un resumen
        conciso y útil, destacando los puntos más relevantes."""
        
        results_text = "\n\n".join([
            f"Título: {r['title']}\nDescripción: {r['description']}\nURL: {r['url']}"
            for r in results
        ])
        
        prompt = f"""Analiza los siguientes resultados de búsqueda para la consulta: "{query}"

Resultados:
{results_text}

Por favor, proporciona:
1. Un resumen general de los resultados
2. Los puntos más importantes encontrados
3. Cualquier patrón o tendencia notable
4. Recomendaciones basadas en la información"""
        
        return await self.generate_response(prompt, system_prompt)
    
    async def generate_markdown(
        self,
        content: str,
        format_type: str = "article"
    ) -> str:
        """
        Genera contenido en formato Markdown usando Claude.
        
        Args:
            content: Contenido a formatear
            format_type: Tipo de formato deseado (article, documentation, etc.)
            
        Returns:
            Contenido formateado en Markdown
        """
        system_prompt = f"""Eres un experto en formato Markdown.
        Tu tarea es convertir el contenido proporcionado en un documento Markdown
        bien estructurado del tipo: {format_type}."""
        
        prompt = f"""Convierte el siguiente contenido en un documento Markdown
        del tipo {format_type}:

{content}

Asegúrate de:
1. Usar los encabezados apropiados
2. Formatear listas y tablas correctamente
3. Incluir enlaces cuando sea relevante
4. Mantener un estilo consistente"""
        
        return await self.generate_response(prompt, system_prompt) 