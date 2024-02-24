from bson import ObjectId
from pymongo import MongoClient
import pytest
from datetime import datetime
from src.common.config import config
from src.common.models.message import Message
from src.data_server.impl.services.db.mongo_message_db import MongoMessageDB


@pytest.fixture
def mongo_message_db() -> MongoMessageDB:
    mongo_client = MongoClient(config["MONGO_URI"])
    db = MongoMessageDB(mongo_client, test=True)
    db.empty_db_for_tests()
    return db


def test_insert_with_text(mongo_message_db):
    sender_id = "user_1"
    receiver_id = "user_2"
    text = "Test message"
    message = mongo_message_db.insert(sender_id, receiver_id, text)

    assert message.sender == str(sender_id)
    assert message.reciever == str(receiver_id)
    assert message.text == text
    assert isinstance(message.time_stamp, datetime)


def test_insert_with_photo_id(mongo_message_db):
    sender_id = "user_1"
    receiver_id = "user_2"
    photo_id = f"{ObjectId()}"
    message = mongo_message_db.insert(sender_id, receiver_id, None, photo_id)

    assert message.sender == str(sender_id)
    assert message.reciever == str(receiver_id)
    assert message.photo_id == str(photo_id)
    assert isinstance(message.time_stamp, datetime)


def test_findOne_returns_message(mongo_message_db):
    message_data = {
        "sender": str("user_1"),
        "reciever": str("user_2"),
        "text": "message text",
    }

    message = mongo_message_db.insert(
        message_data["sender"], message_data["reciever"], message_data["text"]
    )

    result = mongo_message_db.findOne(message.id)

    assert isinstance(result, Message)
    assert result.sender == str(message_data["sender"])
    assert result.reciever == str(message_data["reciever"])
    assert isinstance(result.time_stamp, datetime)


def test_findOne_returns_none_when_not_found(mongo_message_db):

    result = mongo_message_db.findOne(f"{ObjectId()}")

    assert not result


def test_findMany_returns_messages(mongo_message_db):
    sender_id = str("user_1")
    reciever_id = str("user_2")
    mongo_message_db.insert(sender_id, reciever_id, "random text 1")
    mongo_message_db.insert(reciever_id, sender_id, "random text 2")

    result = mongo_message_db.findMany((sender_id, reciever_id))

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(message, Message) for message in result)
