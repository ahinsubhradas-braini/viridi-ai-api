# rate_limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse

# Connect to Redis rate-limiter-db for rate limits
REDIS_URL = "redis://redis-throttling-master:6379"

# Create limiter with Redis storage
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{REDIS_URL}"
)

# Exception handler for 429 errors
def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )

# Generic decorator for rate limits
def limit_request(limit: str):
    """
    Example: @limit_request("5/minute")
    Supports: "10/second", "100/hour", etc.
    """
    return limiter.limit(limit)
