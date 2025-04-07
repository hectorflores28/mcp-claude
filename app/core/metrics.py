from typing import Dict, Optional
from datetime import datetime
import time
from prometheus_client import Counter, Histogram, Gauge
from app.core.logging import LogManager

class ClaudeMetrics:
    """Sistema de métricas para Claude API"""
    
    def __init__(self):
        self.logger = LogManager.get_logger("claude_metrics")
        
        # Contadores
        self.requests_total = Counter(
            'claude_requests_total',
            'Total de solicitudes a Claude API',
            ['endpoint', 'model']
        )
        
        self.tokens_total = Counter(
            'claude_tokens_total',
            'Total de tokens procesados',
            ['type', 'model']
        )
        
        # Histogramas
        self.request_duration = Histogram(
            'claude_request_duration_seconds',
            'Duración de las solicitudes a Claude API',
            ['endpoint', 'model'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        # Gauges
        self.active_requests = Gauge(
            'claude_active_requests',
            'Número de solicitudes activas',
            ['model']
        )
        
        self.rate_limit_remaining = Gauge(
            'claude_rate_limit_remaining',
            'Solicitudes restantes en el límite de tasa',
            ['model']
        )
    
    def track_request_start(self, endpoint: str, model: str) -> None:
        """Registra el inicio de una solicitud"""
        self.active_requests.labels(model=model).inc()
        self.requests_total.labels(endpoint=endpoint, model=model).inc()
        self.logger.debug(f"Iniciando solicitud a {endpoint} con modelo {model}")
    
    def track_request_end(self, endpoint: str, model: str, duration: float) -> None:
        """Registra el fin de una solicitud"""
        self.active_requests.labels(model=model).dec()
        self.request_duration.labels(endpoint=endpoint, model=model).observe(duration)
        self.logger.debug(f"Finalizando solicitud a {endpoint} con modelo {model} en {duration:.2f}s")
    
    def track_tokens(self, count: int, token_type: str, model: str) -> None:
        """Registra el uso de tokens"""
        self.tokens_total.labels(type=token_type, model=model).inc(count)
        self.logger.debug(f"Tokens {token_type} utilizados: {count} para modelo {model}")
    
    def update_rate_limit(self, remaining: int, model: str) -> None:
        """Actualiza el contador de límite de tasa"""
        self.rate_limit_remaining.labels(model=model).set(remaining)
        self.logger.debug(f"Límite de tasa restante para {model}: {remaining}")
    
    def track_error(self, endpoint: str, model: str, error_type: str) -> None:
        """Registra errores en las solicitudes"""
        self.requests_total.labels(
            endpoint=f"{endpoint}_error_{error_type}",
            model=model
        ).inc()
        self.logger.warning(f"Error en solicitud a {endpoint} con modelo {model}: {error_type}")

# Singleton instance
claude_metrics = ClaudeMetrics() 