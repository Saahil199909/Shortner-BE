import redis

from app.config import REDIS_DB, REDIS_HOST, REDIS_PORT

class RedisConnection:
    def __init__(self) -> None:
        self.redis_host = REDIS_HOST
        self.redis_port = REDIS_PORT
        self.redis_db = REDIS_DB
    
    def redis_connection(self):
        return redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

    