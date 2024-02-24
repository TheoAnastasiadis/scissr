from src.common.models.message import Message
from src.common.queues.message import MessageQueue
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.live_server.domain.services.connections.connection_manager import (
    ConnectionManager,
)
from fastapi import WebSocket
from src.live_server.domain.services.notifications.notification_service import (
    NotificationService,
)


class LiveMessageUseCases:

    def __init__(
        self,
        message_queue: MessageQueue,
        connection_manager: ConnectionManager,
        notification_service: NotificationService,
        subscription_db,
    ):
        self.queue = message_queue
        self.connection_manager = connection_manager
        self.notification_service = notification_service
        self.subscription_db = subscription_db

    async def _notify(self, message: Message):
        self.notification_service.notify(
            message.reciever, message
        )  # we do not need to await this

    async def _publish(self, message: Message):
        await self.connection_manager.publish_message(
            message.reciever, message
        )

    async def consume_messages(self):
        messages = self.q.consume()
        for message in messages:
            await self._publish(message)
            await self._notify(message)

    async def connect(self, caller: APICaller, websocket: WebSocket):
        await self.connection_manager.connect(caller.sub, websocket)

    def disconnect(self, websocket: WebSocket):
        self.connection_manager.disconnect(websocket)

    def subscribe_to_notifications(self, caller: APICaller, subscription):
        self.subscription_db.insert(caller.sub, subscription)
