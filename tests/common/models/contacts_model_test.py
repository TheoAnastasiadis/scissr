from bson import ObjectId
from src.common.models import Contact
import pytest
from datetime import datetime
from pydantic import ValidationError


def test_create_contact():
    contact_data = {
        "parties": (ObjectId(), ObjectId()),
        "last_message": "Hello!",
        "time_stamp": datetime.now(),
    }
    contact = Contact(**contact_data)
    assert contact.parties == (
        str(contact_data["parties"][0]),
        str(contact_data["parties"][1]),
    )
    assert contact.last_message == "Hello!"
    assert isinstance(contact.time_stamp, datetime)


def test_invalid_parties_type():
    with pytest.raises(ValidationError):
        Contact(
            parties="user1", last_message="Hello!", time_stamp=datetime.now()
        )


def test_invalid_last_message_type():
    with pytest.raises(ValidationError):
        Contact(
            parties=("user1", "user2"),
            last_message=123,
            time_stamp=datetime.now(),
        )


def test_missing_fields():
    with pytest.raises(ValidationError):
        Contact()
