from typing import Optional, Set, List
import time
import asyncio
from functools import lru_cache
import logging
from datetime import datetime, timedelta

from app.core.cache import get_cache

logger = logging.getLogger(__name__)

class TokenBlacklist:
    def __init__(self):
        self._cache = get_cache()
        self._prefix = "blacklist:"
        self._batch_size = 1000
        self._cleanup_interval = 3600  # 1 hora
        self._last_cleanup = time.time()

    def _get_key(self, token: str) -> str:
        return f"{self._prefix}{token}"

    async def _cleanup_expired(self):
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return

        try:
            # Obtener todas las claves de blacklist
            keys = await self._cache.scan_iter(match=f"{self._prefix}*")
            
            # Procesar en lotes
            for i in range(0, len(keys), self._batch_size):
                batch = keys[i:i + self._batch_size]
                # Verificar expiración
                pipe = self._cache.redis.pipeline()
                for key in batch:
                    pipe.ttl(key)
                ttls = await asyncio.to_thread(lambda: pipe.execute())
                
                # Eliminar tokens expirados
                expired_keys = [k for k, ttl in zip(batch, ttls) if ttl <= 0]
                if expired_keys:
                    await self._cache.delete_many(expired_keys)
            
            self._last_cleanup = current_time
        except Exception as e:
            logger.error(f"Error during blacklist cleanup: {str(e)}")

    async def add_token(self, token: str, expires_in: int) -> bool:
        """
        Agrega un token a la blacklist
        """
        try:
            # Ejecutar limpieza si es necesario
            await self._cleanup_expired()
            
            # Agregar token
            return await self._cache.set(
                self._get_key(token),
                {
                    "added_at": datetime.utcnow().isoformat(),
                    "expires_at": (datetime.utcnow() + timedelta(seconds=expires_in)).isoformat()
                },
                expire=expires_in
            )
        except Exception as e:
            logger.error(f"Error adding token to blacklist: {str(e)}")
            return False

    async def is_blacklisted(self, token: str) -> bool:
        """
        Verifica si un token está en la blacklist
        """
        try:
            # Ejecutar limpieza si es necesario
            await self._cleanup_expired()
            
            # Verificar token
            return await self._cache.get(self._get_key(token)) is not None
        except Exception as e:
            logger.error(f"Error checking blacklisted token: {str(e)}")
            return True  # Por seguridad, asumimos que está blacklisteado

    async def remove_token(self, token: str) -> bool:
        """
        Elimina un token de la blacklist
        """
        try:
            return await self._cache.delete(self._get_key(token))
        except Exception as e:
            logger.error(f"Error removing token from blacklist: {str(e)}")
            return False

    async def clear(self) -> bool:
        """
        Limpia toda la blacklist
        """
        try:
            # Obtener todas las claves de blacklist
            keys = await self._cache.scan_iter(match=f"{self._prefix}*")
            
            # Eliminar en lotes
            for i in range(0, len(keys), self._batch_size):
                batch = keys[i:i + self._batch_size]
                await self._cache.delete_many(batch)
            
            return True
        except Exception as e:
            logger.error(f"Error clearing blacklist: {str(e)}")
            return False

    async def get_blacklisted_tokens(self, limit: int = 100) -> List[dict]:
        """
        Obtiene los tokens blacklisteados con su información
        """
        try:
            # Obtener claves
            keys = await self._cache.scan_iter(match=f"{self._prefix}*", count=limit)
            
            # Obtener valores
            values = await self._cache.mget(keys)
            
            # Formatear resultado
            result = []
            for key, value in zip(keys, values):
                if value is not None:
                    token = key.decode().replace(self._prefix, "")
                    result.append({
                        "token": token,
                        "added_at": value["added_at"],
                        "expires_at": value["expires_at"]
                    })
            
            return result
        except Exception as e:
            logger.error(f"Error getting blacklisted tokens: {str(e)}")
            return []

@lru_cache()
def get_blacklist() -> TokenBlacklist:
    return TokenBlacklist() 