from typing import Optional, Any, Dict
import json
import hashlib
from datetime import datetime, timedelta
import redis
from app.core.config import settings
from app.core.logging import LogManager

class ClaudeCache:
    """Sistema de caché para Claude con soporte para respuestas de IA y resultados de búsqueda"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.default_ttl = 3600  # 1 hora por defecto
        
    def _generate_key(self, prefix: str, data: Dict[str, Any]) -> str:
        """Genera una clave única para el caché basada en los datos"""
        data_str = json.dumps(data, sort_keys=True)
        hash_obj = hashlib.sha256(data_str.encode())
        return f"claude:{prefix}:{hash_obj.hexdigest()}"
    
    def get_cached_response(self, prompt: str, model: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Obtiene una respuesta cacheada para un prompt específico"""
        cache_key = self._generate_key("response", {
            "prompt": prompt,
            "model": model,
            **kwargs
        })
        
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            LogManager.log_info("Respuesta encontrada en caché", extra={"key": cache_key})
            return json.loads(cached_data)
        return None
    
    def cache_response(self, prompt: str, response: Dict[str, Any], model: str, ttl: Optional[int] = None, **kwargs):
        """Almacena una respuesta en el caché"""
        cache_key = self._generate_key("response", {
            "prompt": prompt,
            "model": model,
            **kwargs
        })
        
        ttl = ttl or self.default_ttl
        self.redis_client.setex(
            cache_key,
            ttl,
            json.dumps(response)
        )
        LogManager.log_info("Respuesta almacenada en caché", extra={"key": cache_key, "ttl": ttl})
    
    def get_cached_search(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Obtiene resultados de búsqueda cacheados"""
        cache_key = self._generate_key("search", {
            "query": query,
            **kwargs
        })
        
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            LogManager.log_info("Resultados de búsqueda encontrados en caché", extra={"key": cache_key})
            return json.loads(cached_data)
        return None
    
    def cache_search_results(self, query: str, results: Dict[str, Any], ttl: Optional[int] = None, **kwargs):
        """Almacena resultados de búsqueda en el caché"""
        cache_key = self._generate_key("search", {
            "query": query,
            **kwargs
        })
        
        ttl = ttl or self.default_ttl
        self.redis_client.setex(
            cache_key,
            ttl,
            json.dumps(results)
        )
        LogManager.log_info("Resultados de búsqueda almacenados en caché", extra={"key": cache_key, "ttl": ttl})
    
    def invalidate_cache(self, prefix: str, data: Dict[str, Any]):
        """Invalida entradas específicas del caché"""
        cache_key = self._generate_key(prefix, data)
        self.redis_client.delete(cache_key)
        LogManager.log_info("Caché invalidado", extra={"key": cache_key})
    
    def clear_all_cache(self):
        """Limpia todo el caché"""
        keys = self.redis_client.keys("claude:*")
        if keys:
            self.redis_client.delete(*keys)
        LogManager.log_info("Caché limpiado completamente") 