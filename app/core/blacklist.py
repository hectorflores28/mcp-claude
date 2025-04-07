from typing import Optional
from datetime import datetime, timedelta
from app.core.cache import cache
from app.core.logging import LogManager

class TokenBlacklist:
    """
    Maneja la lista negra de tokens usando Redis como almacenamiento
    """
    def __init__(self):
        self.prefix = "blacklist:token:"
        LogManager.log_info("Sistema de lista negra de tokens inicializado")

    async def add_to_blacklist(self, token: str, expires_in: Optional[int] = None) -> bool:
        """
        Agrega un token a la lista negra
        
        Args:
            token: Token a agregar
            expires_in: Tiempo de expiración en segundos (opcional)
        """
        try:
            # Calcular tiempo de expiración
            if expires_in is None:
                # Obtener tiempo de expiración del token
                from app.core.auth import decode_token
                payload = decode_token(token)
                expires_in = payload.get("exp", 0) - int(datetime.utcnow().timestamp())
            
            # Agregar a la lista negra
            return await cache.set(
                f"{self.prefix}{token}",
                {"blacklisted_at": datetime.utcnow().isoformat()},
                ttl=expires_in
            )
        except Exception as e:
            LogManager.log_error("blacklist", f"Error al agregar token a lista negra: {str(e)}")
            return False

    async def is_blacklisted(self, token: str) -> bool:
        """
        Verifica si un token está en la lista negra
        
        Args:
            token: Token a verificar
        """
        try:
            return await cache.exists(f"{self.prefix}{token}")
        except Exception as e:
            LogManager.log_error("blacklist", f"Error al verificar token en lista negra: {str(e)}")
            return True  # Por seguridad, asumimos que está en la lista negra

    async def remove_from_blacklist(self, token: str) -> bool:
        """
        Elimina un token de la lista negra
        
        Args:
            token: Token a eliminar
        """
        try:
            return await cache.delete(f"{self.prefix}{token}")
        except Exception as e:
            LogManager.log_error("blacklist", f"Error al eliminar token de lista negra: {str(e)}")
            return False

    async def clear_blacklist(self) -> bool:
        """
        Limpia toda la lista negra
        """
        try:
            # Obtener todas las claves de la lista negra
            keys = await cache.redis_client.keys(f"{self.prefix}*")
            if keys:
                return await cache.redis_client.delete(*keys)
            return True
        except Exception as e:
            LogManager.log_error("blacklist", f"Error al limpiar lista negra: {str(e)}")
            return False

# Instancia global de la lista negra
blacklist = TokenBlacklist() 