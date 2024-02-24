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

    def update(
        self, parties_uuids: tuple[str, str], last_message: str
    ) -> Contact:
        result = self.collection.find_one_and_update(
            {
                "parties": {
                    "$all": [
                        {"$elemMatch": {"$eq": elem}} for elem in parties_uuids
                    ]
                }
            },
            {
                "$set": {
                    "last_message": last_message,
                    "time_stamp": datetime.now(),
                    "parties": parties_uuids,
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return Contact(**result)

    def findMany(self, user_uuid: str, skip: int, limit: int) -> list[Contact]:
        query = {"parties": {"$in": [user_uuid]}}
        contacts = (
            self.collection.find(query)
            .sort("time_stamp")
            .limit(limit)
            .skip(skip)
        )
        return [Contact(**contact) for contact in contacts]

    def remove(self, pair_uuids: tuple[str, str]):
        self.collection.delete_many({"parties": {"$all": pair_uuids}})
