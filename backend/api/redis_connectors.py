import redis

from settings import REDIS_URL


class RedisConnectors:
    email_manager_conn = redis.from_url(REDIS_URL + '/0')
