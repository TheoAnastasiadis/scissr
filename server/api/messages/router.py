from dataclasses import dataclass, field
from fastapi import APIRouter

tags = ["messages"]


@dataclass
class MessagesRouter:
    data_service: str = field()
    auth_service: str = field()
    router = APIRouter(tags=tags)

    @router.post("/message/{to}")
    async def post_message(to: str):
        pass

    @router.get("/messages/{to}")
    async def get_messages(to: str, limit: int = 20, skip: int = 0):
        limit = min(limit, 20)
        pass
