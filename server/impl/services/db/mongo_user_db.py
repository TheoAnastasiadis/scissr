from pymongo import MongoClient, ReturnDocument
from typing import List
from server.domain.services.db.user import UserDB
from server.domain.models.user import User
from bson.objectid import ObjectId


class MongoUserDB(UserDB):
    _DB = "main"
    _COLLECTION = "users"

    def __init__(self, client: MongoClient):
        super().__init__()
        self.client = client
        self.db = self.client[self._DB]
        self.collection = self.db[self._COLLECTION]

    def findOne(self, id: str) -> User:
        print(id)
        user = self.collection.find_one(ObjectId(id))
        if user:
            return User(**user)
        else:
            return None

    def findMany(
        self,
        skip: int,
        limit: int,
        location: tuple[float, float],
        distance: int,
        active_mtr: dict,
        kinky_mtr: dict,
        exclude_from_results: List[str],
        excluded_from: str,
        only_active: bool,
        vibes: List[str],
    ) -> List[User]:
        query = {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": list(location),
                    },
                    "$maxDistance": distance * 1000,
                }
            },
            "_id": {"$nin": [ObjectId(id) for id in exclude_from_results]},
            "blocked": {"$nin": ObjectId(excluded_from)},
        }
        if only_active:
            query["online_status"] = {"$eq": True}

        if active_mtr:
            query["active_mtr"] = (
                {"$gte": active_mtr["value"]}
                if active_mtr["operation"] == "GE"
                else {"$lte": active_mtr["value"]}
            )

        if kinky_mtr:
            query["kinky_mtr"] = (
                {"$gte": kinky_mtr["value"]}
                if kinky_mtr["operation"] == "GE"
                else {"$lte": kinky_mtr["value"]}
            )

        if len(vibes) > 0:
            query["vibes"] = {"vibes": {"$in": vibes}}

        users = self.collection.find(query).skip(skip).limit(limit)
        return [User(**user) for user in users]

    def delete(self, id: str):
        self.collection.delete_one({"_id": ObjectId(id)})

    def update(self, user: User, location: tuple[float, float] = None):
        update_data = {"$set": user.model_dump(exclude=["id"])}
        if location:
            update_data["$set"]["location"] = location
        return User(
            **self.collection.find_one_and_update(
                {"_id": ObjectId(user.id)},
                update_data,
                return_document=ReturnDocument.AFTER,
            )
        )
