import redis

# Connect to Redis container
REDIS_HOST = "redis"  # service name from docker-compose
REDIS_PORT = 6379

# Logical DB separation
redis_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)