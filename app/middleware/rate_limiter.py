from fastapi import HTTPException, Request
from functools import wraps
import redis
import time
import os

redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def rate_limit(max_requests: int = 10, window: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host
            key = f"rate_limit:{client_ip}:{func.__name__}"
            
            current = redis_client.get(key)
            if current is None:
                redis_client.setex(key, window, 1)
            else:
                if int(current) >= max_requests:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")
                redis_client.incr(key)
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator