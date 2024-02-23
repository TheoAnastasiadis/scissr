from fastapi import APIRouter, Depends
from src.common.models.message import Message
from src.common.queues.message import MessageQueue
from src.data_server.domain.services.auth.auth_serivce import AuthService
from data_server.domain.services.db.contacts import ContactsDB
from data_server.domain.services.db.message import MessageDB
from data_server.domain.services.db.user import UserDB
from data_server.domain.use_cases.messages import MessageUseCases


class MessagesRouter:

    tags = ["messages"]
    message_use_cases: MessageUseCases
    auth_service: AuthService

    def __init__(
        self,
        auth_service: AuthService,
        message_db: MessageDB,
        message_queue: MessageQueue,
        user_db: UserDB,
        contacts_db: ContactsDB,
    ):
        self.message_use_cases = MessageUseCases(
            message_db, message_queue, user_db, contacts_db
        )
        self.auth_service = auth_service

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)
        get_caller = self.auth_service.get_caller

        @router.get("/messages/{to}")
        async def get_messages(
            to: str, limit: int = 20, skip: int = 0, caller=Depends(get_caller)
        ) -> list[Message]:
            return self.message_use_cases.get_messages(
                caller, [caller.sub, to], skip, limit
            )

        @router.post("/messages/{to}")
        async def send_message(
            to,
            caller=Depends(get_caller),
            text: str = None,
            photo_id: str = None,
        ):
            self.message_use_cases.send_message(caller, to, text, photo_id)

        return router
