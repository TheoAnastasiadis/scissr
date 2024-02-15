from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.common.models.message import Message
from .connection_manager import ConnectionManager


class MessagesRouter:

    tags = ["messages"]
    manager: ConnectionManager

    def __init__(
        self,
    ):
        self.manager = ConnectionManager()

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)

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
