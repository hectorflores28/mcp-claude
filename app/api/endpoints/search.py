from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict
from app.services.brave_search import BraveSearchService
from pydantic import BaseModel

router = APIRouter()
brave_search = BraveSearchService()

class SearchResponse(BaseModel):
    results: List[Dict]
    total_results: int
    query: str

@router.get("/", response_model=SearchResponse)
async def search_web(
    query: str = Query(..., description="Término de búsqueda"),
    num_results: int = Query(10, description="Número de resultados a devolver", ge=1, le=50),
    country: str = Query("ES", description="Código de país para resultados"),
    language: str = Query("es", description="Código de idioma para resultados")
):
    """
    Realiza una búsqueda web usando Brave Search API.
    
    Args:
        query: Término de búsqueda
        num_results: Número de resultados a devolver (1-50)
        country: Código de país para resultados
        language: Código de idioma para resultados
        
    Returns:
        Lista de resultados de búsqueda
    """
    try:
        results = await brave_search.get_web_results(query, num_results)
        return SearchResponse(
            results=results,
            total_results=len(results),
            query=query
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar la búsqueda: {str(e)}"
        ) 