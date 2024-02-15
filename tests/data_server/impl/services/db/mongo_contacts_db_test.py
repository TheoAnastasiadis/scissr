from datetime import datetime
from bson import ObjectId
import pytest
from src.common.config import config
from src.common.models.contact import Contact
from src.data_server.impl.services.db.mongo_contacts_db import MongoContactsDB
from pymongo import MongoClient


@pytest.fixture
def mongo_contacts_db() -> MongoContactsDB:
    mongo_client = MongoClient(config["MONGO_URI"])
    db = MongoContactsDB(mongo_client, test=True)
    db.empty_db_for_tests()
    return db


def test_update_adds_or_updates_contact(mongo_contacts_db):
    parties = (str(ObjectId()), str(ObjectId()))
    last_message = "Test message"

    result = mongo_contacts_db.update(parties, last_message)

    assert isinstance(result, Contact)
    assert result.last_message == last_message
    assert isinstance(result.time_stamp, datetime)


def test_findMany_returns_contacts(mongo_contacts_db):
    parties = (str(ObjectId()), str(ObjectId()))
    mongo_contacts_db.update(parties, "last message")

    result = mongo_contacts_db.findMany(parties[0], 0, 20)

    assert isinstance(result, list)
    assert len(result) == 1
    assert all(isinstance(contact, Contact) for contact in result)


def test_remove_deletes_contact(mongo_contacts_db):
    pair = (str(ObjectId()), str(ObjectId()))
    mongo_contacts_db.update(pair, "last message")

    mongo_contacts_db.remove(pair)
    contacts = mongo_contacts_db.findMany(pair[0], 0, 20)
    assert len(contacts) == 0
