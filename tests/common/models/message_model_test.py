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


def test_text_or_photo_id_required():
    with pytest.raises(ValidationError):
        Message(
            id=str(ObjectId()),
            sender=str(ObjectId()),
            reciever=str(ObjectId()),
        )
