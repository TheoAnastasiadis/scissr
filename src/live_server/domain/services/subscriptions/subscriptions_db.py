from bson import ObjectId
from src.live_server.domain.services.subscriptions.subscription_model import (
    Subscription,
)


class SubscriptionsDB:

    def insert(self, subscription: Subscription):
        raise NotImplementedError("SubscriptionsDB.insert()")

    def findMany(self, uuid: str):
        raise NotImplementedError("SubscriptionsDB.findMany()")

    def delete(self, id: ObjectId):
        raise NotImplementedError("SubscriptionsDB.delete()")
