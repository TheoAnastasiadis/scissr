from server.domain.models.user import User


class UserDB:
    def findOne(id: str) -> User:
        raise NotImplementedError("UserDB.findOne()")

    def findMany(
        *, limit: int = 20, skip: int = 0, filters: dict = {}, exclude_list=[]
    ) -> list[User]:
        raise NotImplementedError("UserDB.findMany()")

    def delete(id: str):
        raise NotImplementedError("UserDB.delete()")

    def update(user: User):
        raise NotImplementedError("UserDB.update()")
