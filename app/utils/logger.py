import logging
from logging.handlers import RotatingFileHandler
import os

class ClaudeLogger:
    def __init__(self, name='claude_mcp'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Configurar archivo de log
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = RotatingFileHandler(
            f'{log_dir}/claude_mcp.log',
            maxBytes=1024*1024,  # 1MB
            backupCount=5
        )
        
        # Formato del log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def log_request(self, prompt, response_time):
        self.logger.info(f"Prompt: {prompt[:100]}... | Response Time: {response_time}s")
    
    def log_error(self, error_msg, exception=None):
        self.logger.error(f"Error: {error_msg}", exc_info=exception) 