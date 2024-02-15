from fastapi import APIRouter, Request
from src.common.models.user import User
from data_server.domain.services.db.auth import AuthDB
from data_server.domain.services.db.contacts import ContactsDB
from data_server.domain.services.db.user import UserDB
from data_server.domain.services.use_cases.user import UserUseCases, Filters


class UserRouter:

    tags = ["users"]
    user_use_cases: UserUseCases

    def __init__(
        self, user_db: UserDB, auth_db: AuthDB, contacts_db: ContactsDB
    ):
        self.user_use_cases = UserUseCases(
            user_db=user_db, auth_db=auth_db, contacts_db=contacts_db
        )

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)

        @router.get("/user/{id}")
        async def get_user(id: str, request: Request) -> User:
            return self.user_use_cases.get_user(request.user, id)

        @router.get("/users/{lat}/{lon}")
        async def get_users(
            lat: float,
            lon: float,
            request: Request,
            skip: int = 0,
            limit: int = 20,
        ) -> list[User]:
            return self.user_use_cases.get_users(
                request.user, Filters(), skip, limit
            )

        @router.post("/user/{id}")
        async def update_user(id: str, body, request: Request) -> User:
            return self.user_use_cases.update_user(request.user, id, body)

        @router.delete("/user/{id}/")
        async def delete_user(id: str, request: Request):
            return self.user_use_cases.delete_user(request.user, id)

        @router.post("/block/user/{id}")
        async def block_user(id: str, request: Request):
            return self.user_use_cases.block_user(request.user, id)

        @router.post("unblock/user/{id}")
        async def unblock_user(id: str, request: Request):
            return self.user_use_cases.unblock_user(request.user, id)

        return router
