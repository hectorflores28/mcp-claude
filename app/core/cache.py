from typing import Optional, Any, Dict, Union, List
import json
import hashlib
from datetime import datetime, timedelta
import redis
from app.core.config import settings
from app.core.logging import LogManager
import time
from functools import wraps, lru_cache
import asyncio
import pickle
from abc import ABC, abstractmethod
from redis.exceptions import RedisError, ConnectionError, TimeoutError
import logging
import backoff

logger = logging.getLogger(__name__)

class CacheBackend(ABC):
    """Clase base abstracta para backends de caché"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor de la caché"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Almacena un valor en la caché"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Elimina un valor de la caché"""
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """Limpia toda la caché"""
        pass
    
    @abstractmethod
    async def mget(self, keys: List[str]) -> List[Optional[Any]]:
        """Obtiene múltiples valores de la caché"""
        pass
    
    @abstractmethod
    async def mset(self, mapping: Dict[str, Any], expire: Optional[int] = None) -> bool:
        """Almacena múltiples valores en la caché"""
        pass
    
    @abstractmethod
    async def scan_iter(self, match: str = "*", count: int = 100) -> List[str]:
        """Itera sobre las claves de la caché"""
        pass
    
    @abstractmethod
    async def delete_many(self, keys: List[str]) -> int:
        """Elimina múltiples valores de la caché"""
        pass

class RedisCache(CacheBackend):
    """Backend de caché con Redis"""
    
    def __init__(self):
        """Inicializa el backend de caché con Redis"""
        # Configurar pool de conexiones
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            ssl=settings.REDIS_SSL,
            max_connections=settings.REDIS_MAX_CONNECTIONS or 10,
            decode_responses=False,
            socket_timeout=settings.REDIS_TIMEOUT or 5,
            socket_connect_timeout=settings.REDIS_TIMEOUT or 5,
            retry_on_timeout=True,
            health_check_interval=30
        )
        
        # Crear cliente con pool
        self.redis = redis.Redis(connection_pool=self.pool)
        
        # Verificar conexión
        try:
            self.redis.ping()
            logger.info("Conexión a Redis establecida")
        except RedisError as e:
            logger.error(f"Error al conectar con Redis: {str(e)}")
            raise
    
    @backoff.on_exception(
        backoff.expo,
        (RedisError, ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor de la caché
        
        Args:
            key: Clave a obtener
            
        Returns:
            Valor almacenado o None si no existe
        """
        try:
            value = await asyncio.to_thread(self.redis.get, key)
            if value is None:
                return None
            return pickle.loads(value)
        except Exception as e:
            logger.error(f"Error al obtener valor de caché: {str(e)}")
            return None
    
    @backoff.on_exception(
        backoff.expo,
        (RedisError, ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        Almacena un valor en la caché
        
        Args:
            key: Clave a almacenar
            value: Valor a almacenar
            expire: Tiempo de expiración en segundos
            
        Returns:
            True si se almacenó correctamente
        """
        try:
            serialized = pickle.dumps(value)
            if expire:
                return await asyncio.to_thread(self.redis.setex, key, expire, serialized)
            return await asyncio.to_thread(self.redis.set, key, serialized)
        except Exception as e:
            logger.error(f"Error al almacenar valor en caché: {str(e)}")
            return False
    
    @backoff.on_exception(
        backoff.expo,
        (RedisError, ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def delete(self, key: str) -> bool:
        """
        Elimina un valor de la caché
        
        Args:
            key: Clave a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        try:
            return await asyncio.to_thread(self.redis.delete, key) > 0
        except Exception as e:
            logger.error(f"Error al eliminar valor de caché: {str(e)}")
            return False
    
    @backoff.on_exception(
        backoff.expo,
        (RedisError, ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def clear(self) -> bool:
        """
        Limpia toda la caché
        
        Returns:
            True si se limpió correctamente
        """
        try:
            return await asyncio.to_thread(self.redis.flushdb)
        except Exception as e:
            logger.error(f"Error al limpiar caché: {str(e)}")
            return False
    
    @backoff.on_exception(
        backoff.expo,
        (RedisError, ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def mget(self, keys: List[str]) -> List[Optional[Any]]:
        """
        Obtiene múltiples valores de la caché
        
        Args:
            keys: Lista de claves a obtener
            
        Returns:
            Lista de valores almacenados
        """
        try:
            if not keys:
                return []
            
            values = await asyncio.to_thread(self.redis.mget, keys)
            result = []
            
            for value in values:
                if value is None:
                    result.append(None)
                else:
                    try:
                        result.append(pickle.loads(value))
                    except Exception:
                        result.append(None)
            
            return result
        except Exception as e:
            logger.error(f"Error al obtener múltiples valores de caché: {str(e)}")
            return [None] * len(keys)
    
    @backoff.on_exception(
        backoff.expo,
        (RedisError, ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def mset(self, mapping: Dict[str, Any], expire: Optional[int] = None) -> bool:
        """
        Almacena múltiples valores en la caché
        
        Args:
            mapping: Diccionario de claves y valores
            expire: Tiempo de expiración en segundos
            
        Returns:
            True si se almacenaron correctamente
        """
        try:
            if not mapping:
                return True
            
            # Serializar valores
            serialized = {k: pickle.dumps(v) for k, v in mapping.items()}
            
            # Usar pipeline para operaciones en lote
            pipe = self.redis.pipeline()
            
            if expire:
                for key, value in serialized.items():
                    pipe.setex(key, expire, value)
            else:
                pipe.mset(serialized)
            
            await asyncio.to_thread(pipe.execute)
            return True
        except Exception as e:
            logger.error(f"Error al almacenar múltiples valores en caché: {str(e)}")
            return False
    
    @backoff.on_exception(
        backoff.expo,
        (RedisError, ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def scan_iter(self, match: str = "*", count: int = 100) -> List[str]:
        """
        Itera sobre las claves de la caché
        
        Args:
            match: Patrón de búsqueda
            count: Número de claves a obtener por iteración
            
        Returns:
            Lista de claves encontradas
        """
        try:
            cursor = 0
            keys = []
            
            while True:
                cursor, batch = await asyncio.to_thread(
                    self.redis.scan, cursor, match=match, count=count
                )
                keys.extend(batch)
                
                if cursor == 0:
                    break
            
            return keys
        except Exception as e:
            logger.error(f"Error al escanear claves de caché: {str(e)}")
            return []
    
    @backoff.on_exception(
        backoff.expo,
        (RedisError, ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def delete_many(self, keys: List[str]) -> int:
        """
        Elimina múltiples valores de la caché
        
        Args:
            keys: Lista de claves a eliminar
            
        Returns:
            Número de claves eliminadas
        """
        try:
            if not keys:
                return 0
            
            return await asyncio.to_thread(self.redis.delete, *keys)
        except Exception as e:
            logger.error(f"Error al eliminar múltiples valores de caché: {str(e)}")
            return 0

@lru_cache()
def get_cache() -> CacheBackend:
    """
    Obtiene una instancia del backend de caché
    
    Returns:
        Instancia del backend de caché
    """
    return RedisCache()

# Instancia global
cache = get_cache()

class CacheManager:
    """Gestor de caché para MCP-Claude"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not CacheManager._initialized:
            self._backend = None
            CacheManager._initialized = True
    
    def set_backend(self, backend: CacheBackend) -> None:
        self._backend = backend
    
    def get(self, key: str) -> Optional[Any]:
        return self._backend.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        return self._backend.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        return self._backend.delete(key)
    
    def clear(self) -> bool:
        return self._backend.clear()

def cached(ttl: Optional[int] = 3600):
    """
    Decorador para cachear resultados de funciones
    
    Args:
        ttl: Tiempo de vida en segundos
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Crear clave única para la función y sus argumentos
            key_parts = [func.__name__]
            
            # Agregar argumentos posicionales
            for arg in args:
                if isinstance(arg, (str, int, float, bool)):
                    key_parts.append(str(arg))
                elif hasattr(arg, "__dict__"):
                    key_parts.append(str(arg.__dict__))
            
            # Agregar argumentos nombrados
            for k, v in sorted(kwargs.items()):
                if isinstance(v, (str, int, float, bool)):
                    key_parts.append(f"{k}:{v}")
                elif hasattr(v, "__dict__"):
                    key_parts.append(f"{k}:{str(v.__dict__)}")
            
            # Crear clave de caché
            cache_key = hashlib.md5(":".join(key_parts).encode()).hexdigest()
            
            # Intentar obtener del caché
            cache = get_cache()
            cached_result = await cache.get(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            # Ejecutar función y cachear resultado
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, expire=ttl)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Crear clave única para la función y sus argumentos
            key_parts = [func.__name__]
            
            # Agregar argumentos posicionales
            for arg in args:
                if isinstance(arg, (str, int, float, bool)):
                    key_parts.append(str(arg))
                elif hasattr(arg, "__dict__"):
                    key_parts.append(str(arg.__dict__))
            
            # Agregar argumentos nombrados
            for k, v in sorted(kwargs.items()):
                if isinstance(v, (str, int, float, bool)):
                    key_parts.append(f"{k}:{v}")
                elif hasattr(v, "__dict__"):
                    key_parts.append(f"{k}:{str(v.__dict__)}")
            
            # Crear clave de caché
            cache_key = hashlib.md5(":".join(key_parts).encode()).hexdigest()
            
            # Intentar obtener del caché
            cache = get_cache()
            cached_result = cache.get(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            # Ejecutar función y cachear resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)
            
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator

class ClaudeCache:
    """Caché especializado para Claude"""
    
    def __init__(self):
        self._cache = get_cache()
    
    def _generate_key(self, prefix: str, data: Dict[str, Any]) -> str:
        """Genera una clave de caché para Claude"""
        key_parts = [prefix]
        for k, v in sorted(data.items()):
            if isinstance(v, (str, int, float, bool)):
                key_parts.append(f"{k}:{v}")
        return hashlib.md5(":".join(key_parts).encode()).hexdigest()
    
    def get_cached_response(self, prompt: str, model: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Obtiene una respuesta cacheada de Claude"""
        key = self._generate_key("claude:response", {
            "prompt": prompt,
            "model": model,
            **kwargs
        })
        return self._cache.get(key)
    
    def cache_response(self, prompt: str, response: Dict[str, Any], model: str, ttl: Optional[int] = None, **kwargs):
        """Cachea una respuesta de Claude"""
        key = self._generate_key("claude:response", {
            "prompt": prompt,
            "model": model,
            **kwargs
        })
        self._cache.set(key, response, ttl=ttl)
    
    def get_cached_search(self, query: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Obtiene resultados de búsqueda cacheados"""
        key = self._generate_key("claude:search", {
            "query": query,
            **kwargs
        })
        return self._cache.get(key)
    
    def cache_search_results(self, query: str, results: Dict[str, Any], ttl: Optional[int] = None, **kwargs):
        """Cachea resultados de búsqueda"""
        key = self._generate_key("claude:search", {
            "query": query,
            **kwargs
        })
        self._cache.set(key, results, ttl=ttl)
    
    def invalidate_cache(self, prefix: str, data: Dict[str, Any]):
        """Invalida entradas de caché específicas"""
        key = self._generate_key(prefix, data)
        self._cache.delete(key)
    
    def clear_all_cache(self):
        """Limpia toda la caché de Claude"""
        self._cache.clear() 