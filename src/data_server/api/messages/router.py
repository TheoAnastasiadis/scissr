from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from src.common.models.message import Message
from src.common.queues.message import MessageQueue
from data_server.domain.services.db.auth import AuthDB
from data_server.domain.services.db.contacts import ContactsDB
from data_server.domain.services.db.message import MessageDB
from data_server.domain.services.db.user import UserDB
from data_server.domain.services.use_cases.messages import MessageUseCases
from .connection_manager import ConnectionManager


class MessagesRouter:

    tags = ["messages"]
    message_use_cases: MessageUseCases
    manager: ConnectionManager

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
        self.manager = ConnectionManager()

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

        @router.websocket("/messages/{from_id}/{to_id}")
        async def subscribe_to_messages(
            websocket: WebSocket,
            from_id: str,
            to_id: str,
        ):
            # once, on opening the websoccket
            await self.manager.register(from_id, to_id, websocket)

            try:
                while True:
                    messages: list[Message] = (
                        self.message_use_cases.get_live_messages()
                    )
                    for message in messages:
                        self.manager.notify(
                            message.sender,
                            message.reciever,
                            message,
                            websocket,
                        )
            except WebSocketDisconnect:
                self.manager.delete(websocket)

        return router
