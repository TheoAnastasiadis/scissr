from src.common.models.user import User


class UserCache:

    def cache_has(self, filters: dict, location: str) -> bool:
        raise NotImplementedError("UserCache.has()")

    def cache_get(self, filters: dict, location: str) -> list[User]:
        raise NotImplementedError("UserCache.get()")

    def cache_set(self, filters: dict, users: list, location: str):
        raise NotImplementedError("UserCache.set()")
