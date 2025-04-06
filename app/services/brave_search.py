import requests
from typing import Dict, List, Optional
from app.core.config import settings

class BraveSearchService:
    def __init__(self):
        self.api_key = settings.BRAVE_API_KEY
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
    
    async def search(
        self,
        query: str,
        num_results: int = 10,
        offset: int = 0,
        country: str = "ES",
        language: str = "es"
    ) -> Dict:
        """
        Realiza una búsqueda web usando Brave Search API.
        
        Args:
            query: Término de búsqueda
            num_results: Número de resultados a devolver
            offset: Desplazamiento para paginación
            country: Código de país para resultados
            language: Código de idioma para resultados
            
        Returns:
            Dict con los resultados de la búsqueda
        """
        params = {
            "q": query,
            "count": num_results,
            "offset": offset,
            "country": country,
            "language": language
        }
        
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status": "error",
                "results": []
            }
    
    async def get_web_results(
        self,
        query: str,
        num_results: int = 10
    ) -> List[Dict]:
        """
        Obtiene resultados web formateados.
        
        Args:
            query: Término de búsqueda
            num_results: Número de resultados a devolver
            
        Returns:
            Lista de resultados formateados
        """
        search_results = await self.search(query, num_results)
        
        if "error" in search_results:
            return []
            
        formatted_results = []
        for result in search_results.get("web", {}).get("results", []):
            formatted_results.append({
                "title": result.get("title", ""),
                "description": result.get("description", ""),
                "url": result.get("url", ""),
                "source": result.get("source", ""),
                "published_date": result.get("published_date", "")
            })
            
        return formatted_results 