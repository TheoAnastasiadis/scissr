from bson import ObjectId
import pytest
from mongomock import MongoClient
from src.common.models.user import User
from src.data_server.impl.services.db.mongo_user_db import MongoUserDB


@pytest.fixture
def mongo_client():
    return MongoClient()


@pytest.fixture
def mongo_user_db(mongo_client):
    return MongoUserDB(mongo_client)


def test_findOne_existing_user(mongo_user_db):
    # Insert test data
    user_data = {
        "username": "test_user",
        "location": (0, 0),
        "age": 35,
        "kinky_mtr": 0.5,
        "active_mtr": 0.5,
    }
    inserted_id = str(
        mongo_user_db.collection.insert_one(user_data).inserted_id
    )

    # Test findOne method
    user = mongo_user_db.findOne(inserted_id)
    assert isinstance(user, User)
    assert user.username == "test_user"
    assert str(user.id) == inserted_id


def test_findOne_nonexistent_user(mongo_user_db):
    user = mongo_user_db.findOne(ObjectId())
    assert user is None


@pytest.mark.skip(
    reason="""NotImplementedError: '$near' is a valid operation but
    it is not supported by Mongomock yet."""
)
def test_findMany(mongo_user_db):
    # Insert test data
    users_data = [
        {
            "username": "user1",
            "location": (0, 0),
            "age": 35,
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user2",
            "location": (1, 1),
            "age": 35,
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
        {
            "username": "user3",
            "location": (2, 2),
            "age": 35,
            "kinky_mtr": 0.5,
            "active_mtr": 0.5,
        },
    ]
    mongo_user_db.collection.insert_many(users_data)

    # Test findMany method
    users = mongo_user_db.findMany(
        0,
        2,
        (0, 0),
        100,
        {0, "GE"},
        {0, "GE"},
        [str(ObjectId())],
        str(ObjectId),
        True,
        ["cats"],
    )

    assert len(users) == 2


def test_delete(mongo_user_db):
    # Insert test data
    user_data = {
        "username": "user_to_be_deleted",
        "location": (2, 2),
        "age": 35,
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
        "kinky_mtr": 0.5,
        "active_mtr": 0.5,
        "location": (0, 0),
        "age": 35,
    }
    # Create a new user object to update
    inserted_id = mongo_user_db.collection.insert_one(user_data).inserted_id
    user = mongo_user_db.findOne(str(inserted_id))

    user.username = "updated_user"
    updated_user = mongo_user_db.update(user)
    # Check if the user has been updated in the database
    assert updated_user.username == "updated_user"


if __name__ == "__main__":
    pytest.main()
