from loguru import logger
from redis import StrictRedis, ConnectionError


class RedisConnector(object):

    def __init__(self, redis_url, expire_time=60*60*24*3):
        self.expire_time = expire_time
        self.redis_db = StrictRedis.from_url(redis_url, decode_responses=True)
        self.ping()

    def ping(self):
        """check redis connect success"""
        try:
            self.redis_db.ping()
        except (Exception,):
            raise ConnectionError('connect to redis failed')

    def key_exist(self, redis_key):
        """check redis key exist"""
        try:
            return self.redis_db.exists(redis_key)
        except (Exception,):
            logger.error('exist: redis error')
            return False

    def hash_get_all(self, redis_key):
        """search all hash values by redis key"""
        try:
            result = self.redis_db.hgetall(redis_key)
        except (Exception,):
            logger.error('hgetall: redis error')
            return {}
        return result

    def hash_mutil_set(self, redis_key, **kwargs):
        try:
            self.redis_db.hmset(redis_key, **kwargs)
            self.redis_db.expire(redis_key, self.expire_time)
        except (Exception,):
            logger.error('hmset: redis error')

    def hash_get(self, redis_key, field):
        """search hash value by redis key and field"""
        try:
            result = self.redis_db.hget(redis_key, field)
        except (Exception,):
            logger.error('hget: redis error')
            return ''
        return result

    def hash_set(self, redis_key, field, value):
        """save hash value by redis key and field"""
        try:
            self.redis_db.hset(redis_key, field, value)
            self.redis_db.expire(redis_key, self.expire_time)
        except (Exception,):
            logger.error('hset: redis error')

    def delete_key(self, redis_key):
        """delete redis key"""
        status = self.redis_db.delete(redis_key)
        return status == 1

