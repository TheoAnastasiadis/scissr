from src.common.models.user import User
from src.common.queues.message import MessageQueue
from src.data_server.domain.services.auth import AuthDB
from src.data_server.domain.services.db.contacts import ContactsDB
from src.data_server.domain.services.db.message import MessageDB
from src.data_server.domain.services.db.user import UserDB
from src.data_server.domain.use_cases.messages import MessageUseCases
import pytest
from fastapi import HTTPException


class MockAuthDB(AuthDB):
    def user_is_admin(self, user_id) -> bool:
        return user_id == "admin"


class MockMessageDB(MessageDB):
    def findMany(self, parties: tuple[str, str], skip: int, limit: int):
        return []

    def insert(
        self,
        sender_id: str,
        reciever_id: str,
        text: str = None,
        photo_id: str = None,
    ):
        return {"id": "message123"}


class MockMessageQueue(MessageQueue):
    def announce(self, caller_id: str, reciever_id: str, message: dict):
        pass


class MockUserDB(UserDB):
    def findOne(self, id: str):
        return User(
            _id=id,
            username=id,
            age=21,
            email="example@email.com",
            online_status=True,
            location=(0, 0),
            kinky_mtr=0.5,
            active_mtr=0.5,
            vibes=[],
        )


class MockContactsDB(ContactsDB):
    def update(self, parties: tuple[str, str], last_message: str):
        pass


def test_get_messages_admin():
    message_use_cases = MessageUseCases(
        MockAuthDB(),
        MockMessageDB(),
        MockMessageQueue(),
        MockUserDB(),
        MockContactsDB(),
    )
    caller = User(
        _id="admin",
        username="admin",
        age=30,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["friendly"],
    )
    messages = message_use_cases.get_messages(caller, ("user123", "user456"))
    assert messages == []


def test_get_messages_user():
    message_use_cases = MessageUseCases(
        MockAuthDB(),
        MockMessageDB(),
        MockMessageQueue(),
        MockUserDB(),
        MockContactsDB(),
    )
    caller = User(
        _id="user123",
        username="user",
        age=25,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["outgoing"],
    )
    messages = message_use_cases.get_messages(caller, ("user123", "user456"))
    assert messages == []


def test_get_messages_unauthorized():
    message_use_cases = MessageUseCases(
        MockAuthDB(),
        MockMessageDB(),
        MockMessageQueue(),
        MockUserDB(),
        MockContactsDB(),
    )
    caller = User(
        _id="other_user",
        username="other",
        age=28,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["adventurous"],
    )
    with pytest.raises(HTTPException) as exc_info:
        message_use_cases.get_messages(caller, ("user123", "user456"))
    assert exc_info.value.status_code == 403


def test_send_message_blocked():
    message_use_cases = MessageUseCases(
        MockAuthDB(),
        MockMessageDB(),
        MockMessageQueue(),
        MockUserDB(),
        MockContactsDB(),
    )
    caller = User(
        _id="caller123",
        username="caller",
        age=25,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["confident"],
        blocked=["rec1234"],
    )
    with pytest.raises(HTTPException) as exc_info:
        message_use_cases.send_message(caller, "rec1234", "Hello!")
    assert exc_info.value.status_code == 403


def test_send_message_empty_input():
    message_use_cases = MessageUseCases(
        MockAuthDB(),
        MockMessageDB(),
        MockMessageQueue(),
        MockUserDB(),
        MockContactsDB(),
    )
    caller = User(
        _id="caller123",
        username="caller",
        age=25,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["confident"],
    )
    with pytest.raises(HTTPException) as exc_info:
        message_use_cases.send_message(caller, "rec1234")
    assert exc_info.value.status_code == 400


def test_send_message_text():
    message_use_cases = MessageUseCases(
        MockAuthDB(),
        MockMessageDB(),
        MockMessageQueue(),
        MockUserDB(),
        MockContactsDB(),
    )
    caller = User(
        _id="caller123",
        username="caller",
        age=25,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["confident"],
    )
    message_use_cases.send_message(caller, "rec1234", "Hello!")


def test_send_message_photo():
    message_use_cases = MessageUseCases(
        MockAuthDB(),
        MockMessageDB(),
        MockMessageQueue(),
        MockUserDB(),
        MockContactsDB(),
    )
    caller = User(
        _id="caller123",
        username="caller",
        age=25,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["confident"],
    )
    message_use_cases.send_message(caller, "rec1234", photo_id="photo123")
