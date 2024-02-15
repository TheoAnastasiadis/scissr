from fastapi import APIRouter, Request
from src.common.models.message import Message
from src.common.queues.message import MessageQueue
from data_server.domain.services.db.auth import AuthDB
from data_server.domain.services.db.contacts import ContactsDB
from data_server.domain.services.db.message import MessageDB
from data_server.domain.services.db.user import UserDB
from data_server.domain.use_cases.messages import MessageUseCases


class MessagesRouter:

    tags = ["messages"]
    message_use_cases: MessageUseCases

    def __init__(
        self,
        auth_db: AuthDB,
        message_db: MessageDB,
        message_queue: MessageQueue,
        user_db: UserDB,
        contacts_db: ContactsDB,
    ):
        self.message_use_cases = MessageUseCases(
            auth_db, message_db, message_queue, user_db, contacts_db
        )

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)

        @router.get("/messages/{from_id}/{to_id}")
        async def get_messages(
            from_id: str,
            to_id: str,
            request: Request,
            limit: int = 20,
            skip: int = 0,
        ) -> list[Message]:
            return self.message_use_cases.get_persisted_messages(
                request.caller, [from_id, to_id], skip, limit
            )

        @router.post("/messages/{to_id}")
        async def send_message(
            self, to_id: str, body: Message, request: Request
        ):
            self.message_use_cases.send_message(
                request.user, to_id, body.photo_id, body.text
            )

        return router
