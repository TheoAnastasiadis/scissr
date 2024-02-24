from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.common.models.message import Message
from src.common.queues.message import MessageQueue
from src.data_server.domain.services.auth.auth_serivce import (
    APICaller,
    AuthService,
)
from src.live_server.domain.services.connections.connection_manager import (
    ConnectionManager,
)

from src.live_server.domain.services.notifications.notification_service import (
    NotificationService,
)
from src.live_server.domain.services.subscriptions.subscription_model import (
    Subscription,
)
from src.live_server.domain.services.subscriptions.subscriptions_db import (
    SubscriptionsDB,
)
from src.live_server.domain.use_cases.message_use_cases import (
    LiveMessageUseCases,
)


class SubscribeRouter:

    tags = ["subscribe"]

    def __init__(
        self,
        message_queue: MessageQueue,
        connection_manager: ConnectionManager,
        notification_service: NotificationService,
        subscriptions_db: SubscriptionsDB,
        auth_service: AuthService,
    ):
        self.message_use_cases = LiveMessageUseCases(
            message_queue,
            connection_manager,
            notification_service,
            subscriptions_db,
        )
        self.auth_service = auth_service

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)  # type: ignore
        get_caller = self.auth_service.get_caller

        @router.websocket("/subscribe/messages/")
        async def subscribe_to_messages(
            websocket: WebSocket,
            caller: APICaller = Depends(get_caller),
        ):
            # once, on opening the websoccket
            await self.message_use_cases.connect(caller, websocket)

            try:
                while True:
                    await self.message_use_cases.consume_messages()
            except WebSocketDisconnect:
                self.message_use_cases.disconnect(websocket)

        @router.post("/subscribe/notifications/")
        async def subscribe_to_notification(
            subscription: Subscription,
            caller: APICaller = Depends(get_caller),
        ):
            self.message_use_cases.subscribe_to_notifications(
                caller, subscription
            )

        return router
