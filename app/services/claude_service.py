from typing import Dict, Any, Optional, List
import anthropic
from app.core.config import settings
from app.core.logging import LogManager
from app.core.prompts import PromptTemplates
from app.schemas.search import SearchAnalysis
from app.core.markdown_logger import MarkdownLogger

class ClaudeService:
    """
    Servicio para interactuar con Claude API
    """
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
        self.model = settings.CLAUDE_MODEL
        self.max_tokens = settings.CLAUDE_MAX_TOKENS
        self.temperature = settings.CLAUDE_TEMPERATURE
        self.markdown_logger = MarkdownLogger()
    
    async def mcp_completion(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Método específico para la integración con Claude Desktop MCP
        
        Args:
            prompt: Prompt para Claude
            max_tokens: Número máximo de tokens (opcional)
            temperature: Temperatura para la generación (opcional)
            
        Returns:
            Dict con la respuesta de Claude
        """
        try:
            # Usar valores proporcionados o los predeterminados
            tokens = max_tokens or self.max_tokens
            temp = temperature or self.temperature
            
            # Generar respuesta con Claude
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=tokens,
                temperature=temp,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extraer contenido generado
            generated_content = response.content[0].text
            
            # Registrar operación
            LogManager.log_claude_operation(
                "mcp_completion",
                prompt[:100] + "...",
                generated_content[:100] + "..."
            )
            
            return {
                "content": generated_content,
                "model": self.model,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            LogManager.log_error("claude", str(e))
            raise
    
    async def generate_markdown(
        self,
        content: str,
        format_type: str = "article",
        save: bool = False,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Genera contenido en formato Markdown usando Claude
        
        Args:
            content: Contenido a formatear
            format_type: Tipo de formato (article, documentation, etc.)
            save: Si se debe guardar el archivo
            filename: Nombre del archivo a guardar
            
        Returns:
            Dict con el contenido generado y metadata
        """
        try:
            # Obtener prompt para generación
            prompt = PromptTemplates.get_markdown_generation_prompt(
                content=content,
                format_type=format_type
            )
            
            # Generar contenido con Claude
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extraer contenido generado
            generated_content = response.content[0].text
            
            # Registrar operación
            LogManager.log_claude_operation(
                "generate_markdown",
                prompt,
                generated_content
            )
            
            result = {
                "content": generated_content,
                "format_type": format_type,
                "model": self.model
            }
            
            # Guardar archivo si se solicita
            if save and filename:
                await self.markdown_logger.log_file_operation(
                    operation="create",
                    filename=filename,
                    content=generated_content
                )
                result["saved"] = True
                result["filename"] = filename
            
            return result
            
        except Exception as e:
            LogManager.log_error("claude", str(e))
            raise
    
    async def analyze_text(
        self,
        text: str,
        analysis_type: str
    ) -> SearchAnalysis:
        """
        Analiza un texto usando Claude
        
        Args:
            text: Texto a analizar
            analysis_type: Tipo de análisis (summary, concepts, sentiment)
            
        Returns:
            SearchAnalysis con el análisis y metadata
        """
        try:
            # Obtener prompt para análisis
            prompt = PromptTemplates.get_text_analysis_prompt(
                text=text,
                analysis_type=analysis_type
            )
            
            # Generar análisis con Claude
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extraer análisis generado
            analysis_text = response.content[0].text
            
            # Registrar operación
            LogManager.log_claude_operation(
                "analyze_text",
                prompt,
                analysis_text
            )
            
            # Parsear el análisis según el tipo
            if analysis_type == "search_results":
                # Extraer secciones del análisis
                sections = analysis_text.split("\n\n")
                summary = sections[0] if sections else ""
                key_points = []
                relevance_score = 0.0
                suggested_queries = []
                
                for section in sections[1:]:
                    if section.startswith("Puntos clave:"):
                        key_points = [point.strip("- ") for point in section.split("\n")[1:]]
                    elif section.startswith("Puntuación de relevancia:"):
                        try:
                            relevance_score = float(section.split(":")[1].strip())
                        except:
                            relevance_score = 0.0
                    elif section.startswith("Consultas sugeridas:"):
                        suggested_queries = [query.strip("- ") for query in section.split("\n")[1:]]
                
                return SearchAnalysis(
                    summary=summary,
                    key_points=key_points,
                    relevance_score=relevance_score,
                    suggested_queries=suggested_queries
                )
            else:
                # Para otros tipos de análisis, devolver el texto completo
                return SearchAnalysis(
                    summary=analysis_text,
                    key_points=[],
                    relevance_score=0.0,
                    suggested_queries=[]
                )
            
        except Exception as e:
            LogManager.log_error("claude", str(e))
            raise
    
    async def edit_markdown(
        self,
        content: str,
        instructions: str
    ) -> Dict[str, Any]:
        """
        Edita contenido Markdown usando Claude
        
        Args:
            content: Contenido original
            instructions: Instrucciones de edición
            
        Returns:
            Dict con el contenido editado y metadata
        """
        try:
            # Obtener prompt para edición
            prompt = PromptTemplates.get_file_edit_prompt(
                content=content,
                instructions=instructions
            )
            
            # Generar edición con Claude
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extraer contenido editado
            edited_content = response.content[0].text
            
            # Registrar operación
            LogManager.log_claude_operation(
                "edit_markdown",
                prompt,
                edited_content
            )
            
            return {
                "content": edited_content,
                "original_content": content,
                "instructions": instructions,
                "model": self.model
            }
            
        except Exception as e:
            LogManager.log_error("claude", str(e))
            raise 