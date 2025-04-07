from typing import Optional, Set, List, Dict, Any
import time
import asyncio
from functools import lru_cache
import logging
from datetime import datetime, timedelta
import backoff

from app.core.cache import get_cache

logger = logging.getLogger(__name__)

class TokenBlacklist:
    """
    Sistema de lista negra de tokens con soporte para limpieza automática y operaciones en lote
    """
    def __init__(self):
        self._cache = get_cache()
        self._prefix = "blacklist:"
        self._batch_size = 1000
        self._cleanup_interval = 3600  # 1 hora
        self._last_cleanup = time.time()
        self._cleanup_lock = asyncio.Lock()

    def _get_key(self, token: str) -> str:
        """Genera la clave para un token en la blacklist"""
        return f"{self._prefix}{token}"

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=3,
        max_time=5
    )
    async def _cleanup_expired(self):
        """
        Limpia tokens expirados de forma eficiente usando procesamiento en lote
        """
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return

        async with self._cleanup_lock:
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
                        logger.info(f"Limpieza de {len(expired_keys)} tokens expirados")
                
                self._last_cleanup = current_time
            except Exception as e:
                logger.error(f"Error durante limpieza de blacklist: {str(e)}")

    async def add_token(self, token: str, expires_in: int) -> bool:
        """
        Agrega un token a la blacklist con metadatos
        
        Args:
            token: Token a agregar
            expires_in: Tiempo de expiración en segundos
            
        Returns:
            bool: True si se agregó correctamente
        """
        try:
            # Ejecutar limpieza si es necesario
            await self._cleanup_expired()
            
            # Agregar token con metadatos
            return await self._cache.set(
                self._get_key(token),
                {
                    "added_at": datetime.utcnow().isoformat(),
                    "expires_at": (datetime.utcnow() + timedelta(seconds=expires_in)).isoformat(),
                    "token_hash": hash(token)
                },
                expire=expires_in
            )
        except Exception as e:
            logger.error(f"Error al agregar token a blacklist: {str(e)}")
            return False

    async def is_blacklisted(self, token: str) -> bool:
        """
        Verifica si un token está en la blacklist
        
        Args:
            token: Token a verificar
            
        Returns:
            bool: True si el token está blacklisteado
        """
        try:
            # Ejecutar limpieza si es necesario
            await self._cleanup_expired()
            
            # Verificar token
            return await self._cache.get(self._get_key(token)) is not None
        except Exception as e:
            logger.error(f"Error al verificar token en blacklist: {str(e)}")
            return True  # Por seguridad, asumimos que está blacklisteado

    async def remove_token(self, token: str) -> bool:
        """
        Elimina un token de la blacklist
        
        Args:
            token: Token a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            return await self._cache.delete(self._get_key(token))
        except Exception as e:
            logger.error(f"Error al eliminar token de blacklist: {str(e)}")
            return False

    async def clear(self) -> bool:
        """
        Limpia toda la blacklist
        
        Returns:
            bool: True si se limpió correctamente
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
            logger.error(f"Error al limpiar blacklist: {str(e)}")
            return False

    async def get_blacklisted_tokens(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene los tokens blacklisteados con sus metadatos
        
        Args:
            limit: Límite de tokens a obtener
            
        Returns:
            List[Dict[str, Any]]: Lista de tokens con sus metadatos
        """
        try:
            # Obtener claves
            keys = await self._cache.scan_iter(match=f"{self._prefix}*", count=limit)
            
            # Obtener datos en lotes
            tokens = []
            for i in range(0, len(keys), self._batch_size):
                batch = keys[i:i + self._batch_size]
                batch_data = await self._cache.get_many(batch)
                
                for key, data in batch_data.items():
                    if data:
                        token = key.replace(self._prefix, "")
                        tokens.append({
                            "token": token,
                            "added_at": data.get("added_at"),
                            "expires_at": data.get("expires_at")
                        })
            
            return tokens[:limit]
        except Exception as e:
            logger.error(f"Error al obtener tokens blacklisteados: {str(e)}")
            return []

    async def add_tokens(self, tokens: List[Dict[str, Any]]) -> Dict[str, bool]:
        """
        Agrega múltiples tokens a la blacklist
        
        Args:
            tokens: Lista de diccionarios con token y expires_in
            
        Returns:
            Dict[str, bool]: Resultado por cada token
        """
        try:
            # Ejecutar limpieza si es necesario
            await self._cleanup_expired()
            
            # Preparar datos para inserción en lote
            mapping = {}
            for token_data in tokens:
                token = token_data["token"]
                expires_in = token_data.get("expires_in", 3600)
                mapping[self._get_key(token)] = {
                    "added_at": datetime.utcnow().isoformat(),
                    "expires_at": (datetime.utcnow() + timedelta(seconds=expires_in)).isoformat(),
                    "token_hash": hash(token)
                }
            
            # Insertar en lote
            success = await self._cache.set_many(mapping)
            
            # Preparar resultado
            results = {}
            for token_data in tokens:
                token = token_data["token"]
                results[token] = success
            
            return results
        except Exception as e:
            logger.error(f"Error al agregar múltiples tokens a blacklist: {str(e)}")
            return {token["token"]: False for token in tokens}

    async def remove_tokens(self, tokens: List[str]) -> Dict[str, bool]:
        """
        Elimina múltiples tokens de la blacklist
        
        Args:
            tokens: Lista de tokens a eliminar
            
        Returns:
            Dict[str, bool]: Resultado por cada token
        """
        try:
            # Preparar claves
            keys = [self._get_key(token) for token in tokens]
            
            # Eliminar en lote
            deleted = await self._cache.delete_many(keys)
            
            # Preparar resultado
            results = {}
            for token in tokens:
                results[token] = deleted > 0
            
            return results
        except Exception as e:
            logger.error(f"Error al eliminar múltiples tokens de blacklist: {str(e)}")
            return {token: False for token in tokens}

# Instancia global de la blacklist
blacklist = TokenBlacklist() 