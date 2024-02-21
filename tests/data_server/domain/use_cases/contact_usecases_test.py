from src.common.models.contact import Contact
from src.common.models.user import User
from src.data_server.domain.services.auth import AuthDB
from src.data_server.domain.services.db.contacts import ContactsDB
from src.data_server.domain.use_cases.contacts import ContactUseCases
import pytest
from fastapi import HTTPException


class MockContactsDB(ContactsDB):
    def findMany(
        self, user_id: str, skip: int = 0, limit: int = 20
    ) -> list[Contact]:
        return []


class MockAuthDB(AuthDB):
    def user_is_admin(self, user_id: str) -> bool:
        return user_id == "admin"


def test_get_contacts_admin():
    contacts_use_cases = ContactUseCases(MockContactsDB(), MockAuthDB())
    caller = User(
        _id="admin",
        username="admin",
        age=30,
        email="example@email.com",
        online_status=True,
        kinky_mtr=0.5,
        active_mtr=0.5,
        location=(0, 0),
        vibes=["friendly"],
    )
    contacts = contacts_use_cases.getContacts(caller, "user123", 0, 20)
    assert contacts == []


def test_get_contacts_user():
    contacts_use_cases = ContactUseCases(MockContactsDB(), MockAuthDB())
    caller = User(
        _id="user123",
        username="user",
        age=25,
        email="example@email.com",
        online_status=True,
        kinky_mtr=0.5,
        active_mtr=0.5,
        location=(0, 0),
        vibes=["outgoing"],
    )
    contacts = contacts_use_cases.getContacts(caller, "user123", 0, 20)
    assert contacts == []


def test_get_contacts_unauthorized():
    contacts_use_cases = ContactUseCases(MockContactsDB(), MockAuthDB())
    caller = User(
        _id="other_user",
        username="other",
        age=28,
        email="example@email.com",
        online_status=True,
        kinky_mtr=0.5,
        active_mtr=0.5,
        location=(0, 0),
        vibes=["adventure"],
    )
    with pytest.raises(HTTPException) as exc_info:
        contacts_use_cases.getContacts(caller, "user123", 0, 20)
    assert exc_info.value.status_code == 403
