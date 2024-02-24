from typing import List
from bson import ObjectId
from mongomock import MongoClient
from src.live_server.domain.services.subscriptions.subscription_model import (
    Subscription,
)
from src.live_server.domain.services.subscriptions.subscriptions_db import (
    SubscriptionsDB,
)


class MongoSubscriptionsDB(SubscriptionsDB):

    _DB = "main"
    _COLLECTION = "subscriptions"

    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client[self._DB]
        self.collection = self.db[self._COLLECTION]

    def insert(self, subscription: Subscription):
        self.collection.insert_one(subscription)

    def findMany(self, uuid: str) -> List[Subscription]:
        result = self.collection.find({"user_uuid": uuid})
        return [Subscription(**data) for data in result]

    def delete(self, id: ObjectId):
        self.collection.delete_one({"id": id})
