from typing import Dict, Optional, List
from datetime import datetime
import time
from prometheus_client import Counter, Histogram, Gauge
from app.core.logging import LogManager
from dataclasses import dataclass, field
import json
import threading
import asyncio

@dataclass
class APIMetric:
    """Métrica individual de API"""
    endpoint: str
    method: str
    status_code: int
    response_time: float
    timestamp: datetime = field(default_factory=datetime.now)
    tokens_used: Optional[int] = None
    error_type: Optional[str] = None

@dataclass
class PerformanceMetric:
    """Métrica de rendimiento del sistema"""
    cpu_usage: float
    memory_usage: float
    active_connections: int
    timestamp: datetime = field(default_factory=datetime.now)

class MetricsCollector:
    """Recolector de métricas para MCP-Claude"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.api_metrics: List[APIMetric] = []
            self.performance_metrics: List[PerformanceMetric] = []
            self._initialized = True
    
    def record_api_call(self, metric: APIMetric) -> None:
        """Registra una métrica de API"""
        with self._lock:
            self.api_metrics.append(metric)
            # Mantener solo las últimas 1000 métricas
            if len(self.api_metrics) > 1000:
                self.api_metrics = self.api_metrics[-1000:]
    
    def record_performance(self, metric: PerformanceMetric) -> None:
        """Registra una métrica de rendimiento"""
        with self._lock:
            self.performance_metrics.append(metric)
            # Mantener solo las últimas 100 métricas
            if len(self.performance_metrics) > 100:
                self.performance_metrics = self.performance_metrics[-100:]
    
    def get_api_metrics(self, 
                       start_time: Optional[datetime] = None,
                       end_time: Optional[datetime] = None) -> List[APIMetric]:
        """Obtiene métricas de API filtradas por rango de tiempo"""
        with self._lock:
            metrics = self.api_metrics
            if start_time:
                metrics = [m for m in metrics if m.timestamp >= start_time]
            if end_time:
                metrics = [m for m in metrics if m.timestamp <= end_time]
            return metrics
    
    def get_performance_metrics(self,
                              start_time: Optional[datetime] = None,
                              end_time: Optional[datetime] = None) -> List[PerformanceMetric]:
        """Obtiene métricas de rendimiento filtradas por rango de tiempo"""
        with self._lock:
            metrics = self.performance_metrics
            if start_time:
                metrics = [m for m in metrics if m.timestamp >= start_time]
            if end_time:
                metrics = [m for m in metrics if m.timestamp <= end_time]
            return metrics
    
    def get_api_summary(self) -> Dict:
        """Obtiene un resumen de las métricas de API"""
        with self._lock:
            if not self.api_metrics:
                return {}
            
            total_calls = len(self.api_metrics)
            success_calls = len([m for m in self.api_metrics if 200 <= m.status_code < 300])
            error_calls = total_calls - success_calls
            
            avg_response_time = sum(m.response_time for m in self.api_metrics) / total_calls
            
            endpoint_counts = {}
            for metric in self.api_metrics:
                endpoint_counts[metric.endpoint] = endpoint_counts.get(metric.endpoint, 0) + 1
            
            return {
                "total_calls": total_calls,
                "success_calls": success_calls,
                "error_calls": error_calls,
                "success_rate": (success_calls / total_calls) * 100,
                "average_response_time": avg_response_time,
                "endpoint_distribution": endpoint_counts
            }
    
    def get_performance_summary(self) -> Dict:
        """Obtiene un resumen de las métricas de rendimiento"""
        with self._lock:
            if not self.performance_metrics:
                return {}
            
            latest = self.performance_metrics[-1]
            
            return {
                "current_cpu_usage": latest.cpu_usage,
                "current_memory_usage": latest.memory_usage,
                "current_active_connections": latest.active_connections,
                "timestamp": latest.timestamp.isoformat()
            }

class MetricsMiddleware:
    """Middleware para recolección automática de métricas"""
    
    def __init__(self, app):
        self.app = app
        self.collector = MetricsCollector()
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        start_time = time.time()
        path = scope["path"]
        method = scope["method"]
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_time = time.time() - start_time
                
                metric = APIMetric(
                    endpoint=path,
                    method=method,
                    status_code=status_code,
                    response_time=response_time
                )
                
                self.collector.record_api_call(metric)
                LogManager.log_info(
                    "API_METRIC",
                    f"Endpoint: {path}, Method: {method}, "
                    f"Status: {status_code}, Time: {response_time:.3f}s"
                )
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)

def record_performance_metric():
    """Decorador para registrar métricas de rendimiento de funciones"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            metric = PerformanceMetric(
                cpu_usage=0.0,  # Esto debería ser implementado con psutil
                memory_usage=0.0,  # Esto debería ser implementado con psutil
                active_connections=0  # Esto debería ser implementado con el contador de conexiones
            )
            
            MetricsCollector().record_performance(metric)
            return result
        
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            metric = PerformanceMetric(
                cpu_usage=0.0,  # Esto debería ser implementado con psutil
                memory_usage=0.0,  # Esto debería ser implementado con psutil
                active_connections=0  # Esto debería ser implementado con el contador de conexiones
            )
            
            MetricsCollector().record_performance(metric)
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator

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