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
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    async def clear(self) -> bool:
        pass

class InMemoryCache(CacheBackend):
    """Backend de caché en memoria"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor de la caché en memoria"""
        if key not in self._cache:
            return None
        
        cache_entry = self._cache[key]
        
        # Verificar si ha expirado
        if cache_entry["expires_at"] and time.time() > cache_entry["expires_at"]:
            del self._cache[key]
            return None
        
        return cache_entry["value"]
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Almacena un valor en la caché en memoria"""
        try:
            expires_at = time.time() + ttl if ttl else None
            self._cache[key] = {
                "value": value,
                "expires_at": expires_at
            }
            return True
        except Exception as e:
            LogManager.log_error("CACHE_ERROR", f"Error al almacenar en caché: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Elimina un valor de la caché en memoria"""
        try:
            if key in self._cache:
                del self._cache[key]
            return True
        except Exception as e:
            LogManager.log_error("CACHE_ERROR", f"Error al eliminar de caché: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Limpia toda la caché en memoria"""
        try:
            self._cache.clear()
            return True
        except Exception as e:
            LogManager.log_error("CACHE_ERROR", f"Error al limpiar caché: {str(e)}")
            return False

class FileCache(CacheBackend):
    """Backend de caché en archivos"""
    
    def __init__(self, cache_dir: str = "cache"):
        import os
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> str:
        """Obtiene la ruta del archivo de caché para una clave"""
        import os
        # Usar hash para evitar problemas con caracteres especiales en la clave
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_hash}.json")
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor de la caché en archivos"""
        import os
        import json
        
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
                
            # Verificar si ha expirado
            if data["expires_at"] and time.time() > data["expires_at"]:
                os.remove(cache_path)
                return None
                
            return data["value"]
        except Exception as e:
            LogManager.log_error("CACHE_ERROR", f"Error al leer de caché: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Almacena un valor en la caché en archivos"""
        import os
        import json
        
        try:
            cache_path = self._get_cache_path(key)
            expires_at = time.time() + ttl if ttl else None
            
            data = {
                "value": value,
                "expires_at": expires_at
            }
            
            with open(cache_path, 'w') as f:
                json.dump(data, f)
                
            return True
        except Exception as e:
            LogManager.log_error("CACHE_ERROR", f"Error al escribir en caché: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Elimina un valor de la caché en archivos"""
        import os
        
        try:
            cache_path = self._get_cache_path(key)
            if os.path.exists(cache_path):
                os.remove(cache_path)
            return True
        except Exception as e:
            LogManager.log_error("CACHE_ERROR", f"Error al eliminar de caché: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Limpia toda la caché en archivos"""
        import os
        import shutil
        
        try:
            shutil.rmtree(self.cache_dir)
            os.makedirs(self.cache_dir, exist_ok=True)
            return True
        except Exception as e:
            LogManager.log_error("CACHE_ERROR", f"Error al limpiar caché: {str(e)}")
            return False

class RedisCache(CacheBackend):
    """Backend de caché con Redis"""
    
    def __init__(self):
        self._redis = None
        self._pool = None
        self._max_retries = 3
        self._retry_delay = 0.1  # 100ms
        self._max_retry_delay = 2.0  # 2s
        self._batch_size = 1000
    
    @property
    def redis(self):
        """Obtiene la conexión a Redis con pool de conexiones"""
        if self._redis is None:
            # Configurar pool de conexiones
            self._pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                ssl=settings.REDIS_SSL,
                decode_responses=True,
                max_connections=20,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
            
            # Crear cliente Redis con pool
            self._redis = redis.Redis(connection_pool=self._pool)
            
            # Verificar conexión
            try:
                self._redis.ping()
                logger.info("Conexión a Redis establecida correctamente")
            except (ConnectionError, TimeoutError) as e:
                logger.error(f"Error al conectar con Redis: {str(e)}")
                raise
        
        return self._redis
    
    @backoff.on_exception(
        backoff.expo,
        (ConnectionError, TimeoutError),
        max_tries=3,
        max_time=5
    )
    async def _execute_with_retry(self, operation):
        """Ejecuta una operación con reintentos y backoff exponencial"""
        try:
            return await asyncio.to_thread(operation)
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"Error de conexión a Redis: {str(e)}. Reintentando...")
            raise
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor de Redis"""
        try:
            data = await self._execute_with_retry(lambda: self.redis.get(key))
            if data is None:
                return None
                
            # Deserializar con pickle para objetos complejos
            return pickle.loads(data)
        except Exception as e:
            logger.error(f"Error al obtener de Redis: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Almacena un valor en Redis"""
        try:
            # Serializar con pickle para objetos complejos
            serialized = pickle.dumps(value)
            
            if expire:
                return await self._execute_with_retry(
                    lambda: self.redis.setex(key, expire, serialized)
                )
            else:
                return await self._execute_with_retry(
                    lambda: self.redis.set(key, serialized)
                )
        except Exception as e:
            logger.error(f"Error al almacenar en Redis: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Elimina un valor de Redis"""
        try:
            return await self._execute_with_retry(lambda: self.redis.delete(key) > 0)
        except Exception as e:
            logger.error(f"Error al eliminar de Redis: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Limpia toda la caché de Redis"""
        try:
            return await self._execute_with_retry(lambda: self.redis.flushdb())
        except Exception as e:
            logger.error(f"Error al limpiar Redis: {str(e)}")
            return False
    
    async def mget(self, keys: List[str]) -> List[Optional[Any]]:
        """Obtiene múltiples valores de Redis en una sola operación"""
        try:
            if not keys:
                return []
                
            # Procesar en lotes para evitar sobrecarga
            results = []
            for i in range(0, len(keys), self._batch_size):
                batch = keys[i:i + self._batch_size]
                batch_results = await self._execute_with_retry(
                    lambda: self.redis.mget(batch)
                )
                
                # Deserializar resultados
                for data in batch_results:
                    if data is None:
                        results.append(None)
                    else:
                        results.append(pickle.loads(data))
            
            return results
        except Exception as e:
            logger.error(f"Error al obtener múltiples valores de Redis: {str(e)}")
            return [None] * len(keys)
    
    async def mset(self, mapping: Dict[str, Any], expire: Optional[int] = None) -> bool:
        """Almacena múltiples valores en Redis en una sola operación"""
        try:
            if not mapping:
                return True
                
            # Serializar valores
            serialized_mapping = {
                k: pickle.dumps(v) for k, v in mapping.items()
            }
            
            # Procesar en lotes
            pipe = self.redis.pipeline()
            for i in range(0, len(serialized_mapping), self._batch_size):
                batch = dict(list(serialized_mapping.items())[i:i + self._batch_size])
                
                if expire:
                    for k, v in batch.items():
                        pipe.setex(k, expire, v)
                else:
                    pipe.mset(batch)
                
                await self._execute_with_retry(lambda: pipe.execute())
            
            return True
        except Exception as e:
            logger.error(f"Error al almacenar múltiples valores en Redis: {str(e)}")
            return False
    
    async def scan_iter(self, match: str = "*", count: int = 100) -> List[str]:
        """Iterar sobre las claves de Redis de forma eficiente"""
        try:
            cursor = 0
            keys = []
            
            while True:
                cursor, batch = await self._execute_with_retry(
                    lambda: self.redis.scan(cursor, match=match, count=count)
                )
                keys.extend(batch)
                
                if cursor == 0:
                    break
            
            return keys
        except Exception as e:
            logger.error(f"Error al escanear claves en Redis: {str(e)}")
            return []
    
    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Obtiene múltiples valores y devuelve un diccionario"""
        try:
            values = await self.mget(keys)
            return {k: v for k, v in zip(keys, values) if v is not None}
        except Exception as e:
            logger.error(f"Error al obtener múltiples valores de Redis: {str(e)}")
            return {}
    
    async def set_many(self, mapping: Dict[str, Any], expire: Optional[int] = None) -> bool:
        """Alias para mset para mantener consistencia"""
        return await self.mset(mapping, expire)
    
    async def delete_many(self, keys: List[str]) -> int:
        """Elimina múltiples claves y devuelve el número de claves eliminadas"""
        try:
            if not keys:
                return 0
                
            # Procesar en lotes
            total_deleted = 0
            for i in range(0, len(keys), self._batch_size):
                batch = keys[i:i + self._batch_size]
                deleted = await self._execute_with_retry(
                    lambda: self.redis.delete(*batch)
                )
                total_deleted += deleted
            
            return total_deleted
        except Exception as e:
            logger.error(f"Error al eliminar múltiples claves de Redis: {str(e)}")
            return 0

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

@lru_cache()
def get_cache() -> CacheBackend:
    """
    Obtiene una instancia del backend de caché
    
    Returns:
        Instancia del backend de caché
    """
    # Intentar usar Redis primero
    try:
        cache = RedisCache()
        # Verificar conexión
        cache.redis.ping()
        return cache
    except Exception as e:
        logger.warning(f"No se pudo conectar a Redis: {str(e)}. Usando caché en memoria.")
        return InMemoryCache() 