from datetime import datetime
from bson import ObjectId
from mongomock import MongoClient
from src.data_server.domain.services.db.message import MessageDB
from src.common.models.message import Message


class MongoMessageDB(MessageDB):
    _DB = "main"
    _COLLECTION = "messages"
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

    def insert(
        self,
        sender_uuid: str,
        reciever_uuid: str,
        text: str | None,
        photo_id: str | None = None,
    ) -> Message:
        message_data = {
            "sender": sender_uuid,
            "reciever": reciever_uuid,
            "time_stamp": datetime.now(),
        }
        if text:
            message_data["text"] = text
        if photo_id:
            message_data["photo_id"] = ObjectId(photo_id)

        inserted_id = self.collection.insert_one(message_data).inserted_id
        message_data["_id"] = str(inserted_id)
        return Message(**message_data)

    def findOne(self, id: str) -> Message | None:
        result = self.collection.find_one(ObjectId(id))
        if result:
            return Message(**result)
        else:
            return None

    def findMany(
        self,
        parties_uuids: tuple[str, str],
        skip=0,
        limit=20,
    ) -> list[Message]:

        query = {
            "$or": [
                {
                    "reciever": parties_uuids[0],
                    "sender": parties_uuids[1],
                },
                {
                    "reciever": parties_uuids[1],
                    "sender": parties_uuids[0],
                },
            ]
        }
        messages = (
            self.collection.find(query)
            .sort("time_stamp")
            .skip(skip)
            .limit(limit)
        )
        return [Message(**message) for message in messages]
