import json
import redis
from src.common.models.user import User
from src.data_server.domain.services.cache.user_cache import UserCache


class RedisUserCache(UserCache):

    def __init__(self, client: redis.StrictRedis):
        self.redis_client = client

    def cache_has(self, filters: dict, location: str) -> bool:
        if "only_active" in filters and filters["only_active"]:
            raise TypeError("cannot query cached result for active users")
        key = self._generate_key(filters, location)
        return self.redis_client.exists(key)

    def cache_get(self, filters: dict, location: str) -> list[User]:
        if "only_active" in filters and filters["only_active"]:
            raise TypeError("cannot get cached result for active users")
        key = self._generate_key(filters, location)
        cached_data = self.redis_client.get(key)
        if cached_data:
            return [
                User(**{**user_data, "_id": user_data["id"]})
                for user_data in json.loads(cached_data)
            ]
        else:
            return []

    def cache_set(self, filters: dict, users: list[User], location: str):
        if "only_active" in filters and filters["only_active"]:
            raise TypeError("cannot set cached result for active users")
        key = self._generate_key(filters, location)
        users_json = json.dumps([user.model_dump() for user in users])
        ttl = 3600  # one hour
        self.redis_client.setex(key, ttl, users_json)

    def _generate_key(self, filters: dict, location: str) -> str:
        d = {**filters, location: location}
        return f"user_cache:{json.dumps(d)}"
