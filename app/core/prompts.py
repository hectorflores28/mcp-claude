from typing import Dict, List, Optional
from app.schemas.mcp import MCPPromptTemplate

class PromptTemplates:
    """Clase para gestionar las plantillas de prompts."""
    
    @staticmethod
    def get_templates() -> List[MCPPromptTemplate]:
        """Obtiene todas las plantillas de prompts disponibles."""
        return [
            MCPPromptTemplate(
                name="analisis_busqueda",
                description="Analiza los resultados de una búsqueda web",
                template="""Analiza los siguientes resultados de búsqueda para la consulta: "{query}"

Resultados:
{results}

Por favor, proporciona:
1. Un resumen general de los resultados
2. Los puntos más importantes encontrados
3. Cualquier patrón o tendencia notable
4. Recomendaciones basadas en la información""",
                parameters=["query", "results"]
            ),
            MCPPromptTemplate(
                name="generar_markdown",
                description="Genera contenido en formato Markdown",
                template="""Convierte el siguiente contenido en un documento Markdown
del tipo {format_type}:

{content}

Asegúrate de:
1. Usar los encabezados apropiados
2. Formatear listas y tablas correctamente
3. Incluir enlaces cuando sea relevante
4. Mantener un estilo consistente""",
                parameters=["content", "format_type"]
            ),
            MCPPromptTemplate(
                name="resumen_documento",
                description="Genera un resumen de un documento",
                template="""Genera un resumen conciso del siguiente documento:

{content}

El resumen debe:
1. Capturar los puntos principales
2. Mantener la estructura lógica
3. Ser aproximadamente el 20% de la longitud original
4. Incluir conclusiones clave""",
                parameters=["content"]
            ),
            MCPPromptTemplate(
                name="extraer_conceptos",
                description="Extrae conceptos clave de un texto",
                template="""Extrae los conceptos clave del siguiente texto:

{content}

Para cada concepto:
1. Identifica el término principal
2. Proporciona una definición breve
3. Indica su importancia en el contexto
4. Relaciónalo con otros conceptos mencionados""",
                parameters=["content"]
            )
        ]
    
    @staticmethod
    def get_template(name: str) -> Optional[MCPPromptTemplate]:
        """Obtiene una plantilla específica por nombre."""
        for template in PromptTemplates.get_templates():
            if template.name == name:
                return template
        return None
    
    @staticmethod
    def format_template(name: str, **kwargs) -> Optional[str]:
        """Formatea una plantilla con los parámetros proporcionados."""
        template = PromptTemplates.get_template(name)
        if not template:
            return None
        
        try:
            return template.template.format(**kwargs)
        except KeyError as e:
            return f"Error al formatear la plantilla: {str(e)}" 