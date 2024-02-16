from bson import ObjectId
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.common.models import Message


def test_create_message():
    message_data = {
        "_id": str(ObjectId()),
        "sender": str(ObjectId()),
        "reciever": str(ObjectId()),
        "text": "Hello!",
        "time_stamp": datetime.now(),
    }
    message = Message(**message_data)
    assert message.id == message_data["_id"]
    assert isinstance(message.time_stamp, datetime)


def test_invalid_id_type():
    with pytest.raises(ValidationError):
        Message(
            id=123,
            sender=str(ObjectId()),
            reciever=str(ObjectId()),
            time_stamp=datetime.now(),
        )


def test_invalid_sender_type():
    with pytest.raises(ValidationError):
        Message(
            id=str(ObjectId()),
            sender=123,
            reciever=str(ObjectId()),
            time_stamp=datetime.now(),
        )


def test_invalid_reciever_type():
    with pytest.raises(ValidationError):
        Message(
            id=str(ObjectId()),
            sender=str(ObjectId()),
            reciever=123,
            time_stamp=datetime.now(),
        )


def test_invalid_photo_id_type():
    with pytest.raises(ValidationError):
        Message(
            id=str(ObjectId()),
            sender=str(ObjectId()),
            reciever=str(ObjectId()),
            photo_id=123,
            time_stamp=datetime.now(),
        )


def test_missing_fields():
    with pytest.raises(ValidationError):
        Message()


def test_text_or_photo_id_required():
    with pytest.raises(ValidationError):
        Message(
            id=str(ObjectId()),
            sender=str(ObjectId()),
            reciever=str(ObjectId()),
        )


def test_assert_either_text_or_photo():
    # Test assertion passes when either text or photo_id is provided
    Message.assert_either_text_or_photo({"text": "Hello!"})
    Message.assert_either_text_or_photo({"photo_id": "abc123"})

    # Test assertion fails when neither text nor photo_id is provided
    with pytest.raises(AssertionError):
        Message.assert_either_text_or_photo({})

    # Test assertion passes when both text and photo_id are provided
    Message.assert_either_text_or_photo(
        {"text": "Hello!", "photo_id": "abc123"}
    )
