"""
Plugin de ejemplo para MCP-Claude.

Este plugin demuestra las funcionalidades básicas del sistema de plugins.
"""

from app.core.plugins import Plugin
from app.core.logging import LogManager

logger = LogManager.get_logger("plugins.example")

class ExamplePlugin(Plugin):
    """Plugin de ejemplo."""
    
    def __init__(self):
        """Inicializa el plugin de ejemplo."""
        super().__init__(
            name="example",
            version="1.0.0",
            description="Plugin de ejemplo que demuestra las funcionalidades básicas"
        )
    
    def initialize(self) -> None:
        """Inicializa el plugin."""
        logger.info("Plugin de ejemplo inicializado")
        
        # Registrar hooks
        from app.core.plugins import plugin_manager
        plugin_manager.register_hook("mcp_before_execute", self.before_execute)
        plugin_manager.register_hook("mcp_after_execute", self.after_execute)
        plugin_manager.register_hook("mcp_error", self.on_error)
    
    def shutdown(self) -> None:
        """Apaga el plugin."""
        logger.info("Plugin de ejemplo apagado")
    
    def before_execute(self, *args, **kwargs) -> None:
        """
        Hook ejecutado antes de cada operación MCP.
        
        Args:
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados
        """
        logger.info("Plugin de ejemplo: antes de ejecutar operación MCP")
        logger.debug(f"Argumentos: {args}")
        logger.debug(f"Argumentos nombrados: {kwargs}")
    
    def after_execute(self, *args, **kwargs) -> None:
        """
        Hook ejecutado después de cada operación MCP.
        
        Args:
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados
        """
        logger.info("Plugin de ejemplo: después de ejecutar operación MCP")
        logger.debug(f"Argumentos: {args}")
        logger.debug(f"Argumentos nombrados: {kwargs}")
    
    def on_error(self, error: Exception, *args, **kwargs) -> None:
        """
        Hook ejecutado cuando ocurre un error.
        
        Args:
            error: Excepción que ocurrió
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados
        """
        logger.error(f"Plugin de ejemplo: error en operación MCP: {str(error)}")
        logger.debug(f"Argumentos: {args}")
        logger.debug(f"Argumentos nombrados: {kwargs}") 