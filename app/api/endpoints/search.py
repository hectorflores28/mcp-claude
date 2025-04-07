from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Optional
from app.services.brave_search import BraveSearch
from app.services.claude_service import ClaudeService
from app.core.logging import LogManager
from app.core.security import verify_api_key
from app.schemas.search import SearchResponse, SearchAnalysis
from app.core.markdown_logger import MarkdownLogger

router = APIRouter()
brave_search = BraveSearch()
claude_service = ClaudeService()
markdown_logger = MarkdownLogger()

@router.get("/search", response_model=SearchResponse)
async def search_web(
    query: str = Query(..., description="Término de búsqueda"),
    num_results: int = Query(10, description="Número de resultados a devolver", ge=1, le=50),
    country: str = Query("ES", description="Código de país para resultados"),
    language: str = Query("es", description="Código de idioma para resultados"),
    analyze: bool = Query(False, description="Si se debe analizar los resultados con Claude"),
    api_key: str = Depends(verify_api_key)
):
    """
    Realiza una búsqueda web usando Brave Search API y opcionalmente analiza los resultados con Claude.
    
    Args:
        query: Término de búsqueda
        num_results: Número de resultados a devolver (1-50)
        country: Código de país para resultados
        language: Código de idioma para resultados
        analyze: Si se debe analizar los resultados con Claude
        api_key: API key para autenticación
        
    Returns:
        Lista de resultados de búsqueda y opcionalmente un análisis
    """
    try:
        # Registrar la búsqueda
        markdown_logger.log_search(query, num_results)
        
        # Realizar búsqueda
        results = await brave_search.search(
            query=query,
            num_results=num_results,
            country=country,
            language=language
        )
        
        # Analizar resultados si se solicita
        analysis = None
        if analyze:
            analysis = await claude_service.analyze_text(
                text=str(results),
                analysis_type="search_results"
            )
            
            # Guardar análisis en archivo Markdown
            await markdown_logger.log_file_operation(
                operation="create",
                filename=f"search_analysis_{query.replace(' ', '_')}.md",
                content=analysis.summary
            )
        
        # Registrar resultados
        markdown_logger.log_search_results(query, len(results))
        
        return SearchResponse(
            results=results,
            total_results=len(results),
            query=query,
            analysis=analysis
        )
        
    except Exception as e:
        LogManager.log_error("search", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar la búsqueda: {str(e)}"
        ) 