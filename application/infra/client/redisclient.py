from redis import Redis, ConnectionPool


class Singleton(type):
    """
    A metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):

    def __init__(self, redis_url):
        self.pool = ConnectionPool.from_url(redis_url)

    @property
    def connector(self):
        if not hasattr(self, '_conn'):
            self.get_connection()
        return self._conn

    def get_connection(self):
        self._conn = Redis(connection_pool=self.pool)
