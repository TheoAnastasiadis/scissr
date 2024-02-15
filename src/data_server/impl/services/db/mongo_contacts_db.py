from datetime import datetime
from bson import ObjectId
from mongomock import MongoClient
from pymongo import ReturnDocument
from src.common.models.contact import Contact
from src.data_server.domain.services.db.contacts import ContactsDB


class MongoContactsDB(ContactsDB):

    _DB = "main"
    _COLLECTION = "contacts"
    _TEST = False

    def __init__(self, client: MongoClient, test: bool = False):
        super().__init__()
        self.client = client
        if test:
            self._TEST = True
            self._DB = "test"
        self.db = self.client[self._DB]
        self.collection = self.db[self._COLLECTION]

    def empty_db_for_tests(self):
        if not self._TEST:
            raise ValueError("Cannot empty database if not testing")
        self.collection.delete_many({})

    def update(self, parties: tuple[str, str], last_message: str) -> Contact:
        pair = list(map(lambda p: ObjectId(p), list(parties)))
        result = self.collection.find_one_and_update(
            {
                "parties": {
                    "$all": [{"$elemMatch": {"$eq": elem}} for elem in pair]
                }
            },
            {
                "$set": {
                    "last_message": last_message,
                    "time_stamp": datetime.now(),
                    "parties": pair,
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return Contact(**result)

    def findMany(self, user_id: str, skip: int, limit: int) -> list[Contact]:
        query = {"parties": {"$in": [ObjectId(user_id)]}}
        contacts = (
            self.collection.find(query)
            .sort("time_stamp")
            .limit(limit)
            .skip(skip)
        )
        return [Contact(**contact) for contact in contacts]

    def remove(self, pair: tuple[str, str]):
        pair = list(map(lambda p: ObjectId(p), list(pair)))
        self.collection.delete_many({"parties": {"$all": pair}})
