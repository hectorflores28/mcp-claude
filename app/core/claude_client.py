import os
import time
from ..utils.logger import ClaudeLogger

class ClaudeClient:
    def __init__(self):
        self.logger = ClaudeLogger()
        self.api_key = os.getenv('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY no encontrada en variables de entorno")
    
    def generate_response(self, prompt):
        if not prompt:
            raise ValueError("El prompt no puede estar vacío")
        
        start_time = time.time()
        try:
            # Aquí iría la implementación real con Claude Desktop
            response = "Respuesta de prueba de Claude"
            response_time = time.time() - start_time
            
            self.logger.log_request(prompt, response_time)
            return response
            
        except Exception as e:
            self.logger.log_error("Error al generar respuesta", e)
            raise 