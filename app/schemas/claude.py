from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ClaudeRequest(BaseModel):
    """
    Solicitud para Claude
    """
    text: str = Field(..., description="Texto a analizar")
    analysis_type: Optional[str] = Field(None, description="Tipo de análisis a realizar")
    format_type: Optional[str] = Field("article", description="Tipo de formato para generación de Markdown")
    max_tokens: Optional[int] = Field(4096, description="Número máximo de tokens")
    temperature: Optional[float] = Field(0.7, description="Temperatura para la generación")

class ClaudeResponse(BaseModel):
    """
    Respuesta de Claude
    """
    content: str = Field(..., description="Contenido generado")
    tokens_used: int = Field(..., description="Número de tokens utilizados")
    model: str = Field(..., description="Modelo utilizado")
    analysis: Optional[Dict[str, Any]] = Field(None, description="Resultado del análisis")

class ClaudeAnalysis(BaseModel):
    """
    Análisis de Claude
    """
    summary: str = Field(..., description="Resumen del texto")
    key_points: List[str] = Field(..., description="Puntos clave")
    sentiment: str = Field(..., description="Sentimiento del texto")
    topics: List[str] = Field(..., description="Temas identificados")
    suggestions: List[str] = Field(..., description="Sugerencias de mejora")

class ClaudeToolSchema(BaseModel):
    """
    Esquema de la herramienta de Claude
    """
    name: str = Field("claude", description="Nombre de la herramienta")
    description: str = Field("Análisis y generación de texto usando Claude", description="Descripción de la herramienta")
    parameters: Dict[str, Any] = Field(
        default={
            "text": {"type": "string", "description": "Texto a analizar"},
            "analysis_type": {"type": "string", "description": "Tipo de análisis"},
            "format_type": {"type": "string", "description": "Tipo de formato"},
            "max_tokens": {"type": "integer", "description": "Máximo de tokens"},
            "temperature": {"type": "number", "description": "Temperatura"}
        },
        description="Parámetros de la herramienta"
    ) 