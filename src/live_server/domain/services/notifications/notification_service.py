from src.common.models.message import Message
from src.live_server.domain.services.subscriptions.subscriptions_db import (
    SubscriptionsDB,
)


class NotificationService:

    def __init__(self, subscriptions_db: SubscriptionsDB):
        self.subscriptions_db = subscriptions_db

    async def notify(self, reciever_uuid: str, message: Message):
        subscriptions = self.subscriptions_db.findMany(reciever_uuid)
        for subscription in subscriptions:
            pass  # request on endpoint
