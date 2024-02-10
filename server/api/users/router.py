from fastapi import APIRouter
from dataclasses import dataclass, field
from domain.models.user import User

tags = ["users"]


@dataclass
class UserRouter:
    data_service: str = field()
    auth_service: str = field()
    router = APIRouter(tags=tags)

    @router.get("/user/{id}")
    async def get_user(id: str) -> User:
        pass

    @router.get("/users/{lat}/{lon}")
    async def get_users(
        lat: float, lon: float, skip: int = 0, limit: int = 20
    ) -> list[User]:
        limit = min(limit, 20)
        pass

    @router.post("/user/{id}")
    async def update_user(id: str) -> User:
        pass

    @router.delete("/user/{id}/")
    async def delete_user(id: str):
        pass

    @router.post("/block/user/{id}")
    async def block_user(id: str):
        pass

    @router.post("unblock/user/{id}")
    async def unblock_user(id: str):
        pass
