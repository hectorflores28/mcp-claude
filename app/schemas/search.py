from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class SearchParameters(BaseModel):
    query: str = Field(..., description="Término de búsqueda")
    num_results: int = Field(10, description="Número de resultados a devolver", ge=1, le=50)
    country: str = Field("ES", description="Código de país para resultados")
    language: str = Field("es", description="Código de idioma para resultados")
    analyze: bool = Field(False, description="Si se debe analizar los resultados con Claude")

class SearchResult(BaseModel):
    title: str
    description: str
    url: str
    source: Optional[str] = None
    published_date: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int
    query: str
    analysis: Optional[str] = None

class SearchToolSchema(BaseModel):
    name: str = "buscar_en_brave"
    description: str = "Realiza búsquedas web usando Brave Search API"
    parameters: Dict = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Término de búsqueda"},
            "num_results": {"type": "number", "description": "Número de resultados a devolver"},
            "analyze": {"type": "boolean", "description": "Si se debe analizar los resultados con Claude"}
        }
    } 