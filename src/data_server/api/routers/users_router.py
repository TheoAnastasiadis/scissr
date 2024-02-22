from fastapi import APIRouter, Depends, Request
from src.common.models.user import User

from data_server.domain.services.db.contacts import ContactsDB
from data_server.domain.services.db.user import UserDB
from data_server.domain.use_cases.user import UserUseCases
from src.data_server.domain.services.auth.auth_serivce import AuthService
from src.data_server.domain.services.cache.user_cache import UserCache
from src.data_server.domain.use_cases.models.search_filters import (
    SearchFilters,
)
from src.data_server.domain.use_cases.models.update_body import UpdateUserBody


class UserRouter:

    tags = ["users"]
    user_use_cases: UserUseCases
    auth_service: AuthService

    def __init__(
        self,
        user_db: UserDB,
        user_cache: UserCache,
        contacts_db: ContactsDB,
        auth_service: AuthService,
    ):
        self.user_use_cases = UserUseCases(
            user_db=user_db, user_cache=user_cache, contacts_db=contacts_db
        )
        self.auth_service = auth_service

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)
        get_caller = self.auth_service.get_caller

        @router.get("/profile")
        async def profile(caller=Depends(get_caller)):
            return self.user_use_cases.profile(caller)

        @router.post("/profile/complete")
        async def complete_profile(
            body: UpdateUserBody,
            caller=Depends(get_caller),
        ):
            return self.user_use_cases.complete_profile(caller, body)

        @router.get("/profile/update")
        async def update_profile(
            body: UpdateUserBody, caller=Depends(get_caller)
        ):
            return self.user_use_cases.update_user(caller, body)

        @router.get("/user/{id}")
        async def get_user(id: str, caller=Depends(get_caller)) -> User:
            return self.user_use_cases.get_user(caller, id)

        @router.get("/users")
        async def get_users(
            filters: SearchFilters,
            skip: int = 0,
            limit: int = 20,
            caller=Depends(get_caller),
        ) -> list[User]:
            return self.user_use_cases.get_users(caller, filters, skip, limit)

        @router.post("/block/user/{id}")
        async def block_user(id: str, request: Request):
            return self.user_use_cases.block_user(request.user, id)

        @router.post("unblock/user/{id}")
        async def unblock_user(id: str, request: Request):
            return self.user_use_cases.unblock_user(request.user, id)

        return router
