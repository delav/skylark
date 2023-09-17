from django_redis.client.default import DefaultClient


class RedisClient(DefaultClient):

    def hset(self, key, field, value, version=None, client=None):
        key = self.make_key(key, version=version)
        client = client or self.get_client(write=True)
        return client.hset(key, field, value)

    def hget(self, key, field, version=None, client=None):
        key = self.make_key(key, version=version)
        client = client or self.get_client(write=True)
        return client.hget(key, field)

    def hgetall(self, key, version=None, client=None):
        key = self.make_key(key, version=version)
        client = client or self.get_client(write=True)
        return client.hgetall(key)

    def hdel(self, key, field, version=None, client=None):
        key = self.make_key(key, version=version)
        client = client or self.get_client(write=True)
        return client.hdel(key, field)

    def hlen(self, key, version=None, client=None):
        key = self.make_key(key, version=version)
        client = client or self.get_client(write=True)
        return client.hlen(key)

    def hkeys(self, key, version=None, client=None):
        key = self.make_key(key, version=version)
        client = client or self.get_client(write=True)
        return client.hkeys(key)

    def hexists(self, key, field, version=None, client=None):
        key = self.make_key(key, version=version)
        client = client or self.get_client(write=True)
        return client.hexists(key, field)
