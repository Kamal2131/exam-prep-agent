from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
MCQ_GENERATION_TIME = Histogram('mcq_generation_duration_seconds', 'MCQ generation time')
ACTIVE_USERS = Gauge('active_users_total', 'Number of active users')
EXAM_ATTEMPTS = Counter('exam_attempts_total', 'Total exam attempts', ['status'])

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    status_code = message["status"]
                    duration = time.time() - start_time
                    
                    REQUEST_COUNT.labels(
                        method=scope["method"],
                        endpoint=scope["path"],
                        status=status_code
                    ).inc()
                    
                    REQUEST_DURATION.observe(duration)
                
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)