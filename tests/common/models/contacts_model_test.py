from uuid import uuid4
from bson import ObjectId
from src.common.models import Contact
from datetime import datetime
from pydantic import ValidationError


def test_create_contact():
    contact_data = {
        "_id": str(ObjectId()),
        "parties": (str(uuid4()), str(uuid4())),
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
