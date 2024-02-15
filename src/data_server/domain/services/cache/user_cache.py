from src.common.models.user import User


class UserCache:

    def cache_has(self, filters: dict) -> bool:
        raise NotImplementedError("UserCache.has()")

    def cache_get(self, filters: dict) -> list[User]:
        raise NotImplementedError("UserCache.get()")
