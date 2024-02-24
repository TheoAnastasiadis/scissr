from src.common.models.user import User


class UserDB:
    def findOne(
        self, by_uuid: str | None = None, by_email: str | None = None
    ) -> User:
        raise NotImplementedError("UserDB.findOne()")

    def findMany(
        self,
        skip: int,
        limit: int,
        location: tuple[float, float],
        distance: float,
        active_mtr: dict | None,
        kinky_mtr: dict | None,
        exclude_from_results: list[str],
        excluded_from: str,
        only_active: bool,
        vibes: list[str],
    ) -> list[User]:
        raise NotImplementedError("UserDB.findMany()")

    def delete(self, id: str):
        raise NotImplementedError("UserDB.delete()")

    def update(self, user: User):
        raise NotImplementedError("UserDB.update()")

    def insert(self, user: User):
        raise NotImplementedError("UserDB.insert()")
