from uuid import uuid4
import pytest
from pymongo import MongoClient
from src.common.models.user import User
from src.common.config import config
from src.data_server.impl.services.db.mongo_user_db import MongoUserDB


@pytest.fixture
def mongo_user_db():
    mongo_client = MongoClient(config["MONGO_URI"])
    db = MongoUserDB(mongo_client, test=True)
    db.empty_db_for_tests()
    return db


def test_findOne_existing_user(mongo_user_db):
    # Insert test data
    user_data = {
        "username": "test_user",
        "uuid": str(uuid4()),
        "location": (0, 0),
        "age": 35,
        "email": "email@example.com",
        "kinky_mtr": 0.5,
        "active_mtr": 0.5,
    }
    mongo_user_db.collection.insert_one(user_data)

    # Test findOne method
    user = mongo_user_db.findOne(user_data["uuid"])
    assert isinstance(user, User)
    assert user.username == "test_user"
    assert user.uuid == user_data["uuid"]


def test_findOne_nonexistent_user(mongo_user_db):
    user = mongo_user_db.findOne(str(uuid4()))
    assert user is None


def test_findMany_w_pagination(mongo_user_db):
    # Insert test data
    users_data = [
        {
            "username": "user1",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user2",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user3",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
    ]
    mongo_user_db.collection.insert_many(users_data)

    # Test findMany method
    users = mongo_user_db.findMany(
        skip=0,
        limit=2,
        location=(0, 0),
        distance=100,
        active_mtr={"value": 0, "operation": "GE"},
        kinky_mtr={"value": 0, "operation": "GE"},
        exclude_from_results=[],
        excluded_from=None,
        only_active=False,
        vibes=[],
    )

    assert len(users) == 2


def test_findMany_w_blocked(mongo_user_db):
    # Insert test data
    users_data = [
        {
            "username": "user1",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user2",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user3",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
    ]
    inserted_ids = mongo_user_db.collection.insert_many(
        users_data
    ).inserted_ids

    # the third user has blocked the first
    mongo_user_db.collection.update_one(
        {"_id": inserted_ids[2]}, {"$set": {"blocked": [inserted_ids[0]]}}
    )

    # Test findMany method
    users = mongo_user_db.findMany(
        skip=0,
        limit=20,
        location=(0, 0),
        distance=100,
        active_mtr={"value": 0, "operation": "GE"},
        kinky_mtr={"value": 0, "operation": "GE"},
        exclude_from_results=[inserted_ids[1]],
        excluded_from=str(inserted_ids[0]),
        only_active=False,
        vibes=[],
    )

    assert len(users) == 1


def test_findMany_w_location(mongo_user_db):
    # Insert test data
    users_data = [
        {
            "username": "user1",
            "location": (37.97945, 23.71622),  # Athens
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user2",
            "location": (40.64361, 22.93086),  # Thessaloniki
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user3",
            "location": (52.37403, 4.88969),  # Amsterdam
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
    ]

    mongo_user_db.collection.insert_many(users_data)

    # Test findMany method
    users = mongo_user_db.findMany(
        skip=0,
        limit=20,
        location=(37.97945, 23.71622),  # Athens
        distance=500,  # 500kms
        active_mtr={"value": 0, "operation": "GE"},
        kinky_mtr={"value": 0, "operation": "GE"},
        exclude_from_results=[],
        excluded_from=None,
        only_active=False,
        vibes=[],
    )

    assert len(users) == 2


def test_findMany_w_vibes(mongo_user_db):
    # Insert test data
    users_data = [
        {
            "username": "user1",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
            "vibes": ["cats", "shibari"],
        },
        {
            "username": "user2",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
            "vibes": ["shibari", "hentai"],
        },
        {
            "username": "user3",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
            "vibes": ["cats"],
        },
    ]

    mongo_user_db.collection.insert_many(users_data)

    # Test findMany method
    users = mongo_user_db.findMany(
        skip=0,
        limit=20,
        location=(0, 0),
        distance=100,
        active_mtr={"value": 0, "operation": "GE"},
        kinky_mtr={"value": 0, "operation": "GE"},
        exclude_from_results=[],
        excluded_from=None,
        only_active=False,
        vibes=["shibari"],
    )

    assert len(users) == 2


def test_findMany_w_mtr(mongo_user_db):
    # Insert test data
    users_data = [
        {
            "username": "user1",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.3,
            "active_mtr": 0.6,
        },
        {
            "username": "user2",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.6,
            "active_mtr": 0.2,
        },
        {
            "username": "user3",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.6,
            "active_mtr": 0.6,
        },
    ]

    mongo_user_db.collection.insert_many(users_data)

    # Test findMany method
    users = mongo_user_db.findMany(
        skip=0,
        limit=20,
        location=(0, 0),
        distance=100,
        active_mtr={"value": 0.5, "operation": "GE"},
        kinky_mtr={"value": 0.5, "operation": "GE"},
        exclude_from_results=[],
        excluded_from=None,
        only_active=False,
        vibes=[],
    )

    assert len(users) == 1


def test_findMany_w_status(mongo_user_db):
    # Insert test data
    users_data = [
        {
            "username": "user1",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user2",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user3",
            "location": (0, 0),
            "age": 35,
            "email": "email@example.com",
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
            "online_status": True,
        },
    ]

    mongo_user_db.collection.insert_many(users_data)

    # Test findMany method
    users = mongo_user_db.findMany(
        skip=0,
        limit=20,
        location=(0, 0),
        distance=100,
        active_mtr={"value": 0.5, "operation": "GE"},
        kinky_mtr={"value": 0.5, "operation": "GE"},
        exclude_from_results=[],
        excluded_from=None,
        only_active=True,
        vibes=[],
    )

    assert len(users) == 1


def test_delete(mongo_user_db):
    # Insert test data
    user_data = {
        "username": "user_to_be_deleted",
        "location": (2, 2),
        "age": 35,
        "email": "email@example.com",
        "kinky_mtr": 0.5,
        "active_mtr": 0.5,
    }
    inserted_id = str(
        mongo_user_db.collection.insert_one(user_data).inserted_id
    )

    # Test delete method
    mongo_user_db.delete(inserted_id)

    assert (
        mongo_user_db.collection.find_one({"username": user_data["username"]})
        is None
    )


def test_update(mongo_user_db):

    # create test data
    user_data = {
        "username": "test_user",
        "uuid": str(uuid4()),
        "kinky_mtr": 0.5,
        "active_mtr": 0.5,
        "location": (0, 0),
        "age": 35,
        "email": "email@example.com",
    }
    # Create a new user object to update
    mongo_user_db.collection.insert_one(user_data).inserted_id
    user = mongo_user_db.findOne(user_data["uuid"])

    user.username = "upd_user"
    updated_user = mongo_user_db.update(user)
    # Check if the user has been updated in the database
    assert updated_user.username == "upd_user"


if __name__ == "__main__":
    pytest.main()
