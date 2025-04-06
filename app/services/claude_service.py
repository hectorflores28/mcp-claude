from typing import Dict, Any, Optional
import anthropic
from app.core.config import settings
from app.core.logging import LogManager
from app.core.prompts import PromptTemplates

class ClaudeService:
    """
    Servicio para interactuar con Claude API
    """
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
    
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
                # TODO: Implementar guardado de archivo
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
    ) -> Dict[str, Any]:
        """
        Analiza un texto usando Claude
        
        Args:
            text: Texto a analizar
            analysis_type: Tipo de análisis (summary, concepts, sentiment)
            
        Returns:
            Dict con el análisis y metadata
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
            analysis = response.content[0].text
            
            # Registrar operación
            LogManager.log_claude_operation(
                "analyze_text",
                prompt,
                analysis
            )
            
            return {
                "analysis": analysis,
                "type": analysis_type,
                "model": self.model
            }
            
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