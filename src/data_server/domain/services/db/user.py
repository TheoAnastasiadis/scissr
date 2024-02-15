from src.common.models.user import User


class UserDB:
    def findOne(self, id: str) -> User:
        raise NotImplementedError("UserDB.findOne()")

    def findMany(
        self,
        skip: int,
        limit: int,
        location: tuple[float, float],
        distance: int,
        active_mtr: dict,
        kinky_mtr: dict,
        exclude_from_results: list[str],
        excluded_from: list[str],
        only_active: bool,
        vibes: list[str],
    ) -> list[User]:
        raise NotImplementedError("UserDB.findMany()")

    def delete(self, id: str):
        raise NotImplementedError("UserDB.delete()")

    def update(self, user: User, location: tuple = None):
        raise NotImplementedError("UserDB.update()")
