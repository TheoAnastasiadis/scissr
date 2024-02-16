from datetime import datetime
from src.common.models.message import Message
from src.common.models.user import User
from src.data_server.domain.services.auth import AuthDB
from src.data_server.domain.services.db.message import MessageDB
from src.data_server.domain.services.db.user import UserDB
from src.data_server.domain.services.storage.storage import Storage
from src.data_server.domain.use_cases.photos import PhotoUseCases
import pytest
from fastapi import HTTPException
from bson import ObjectId

sender_id = str(ObjectId())
reciever_id = str(ObjectId())


class MockAuthDB(AuthDB):
    def user_is_admin(self, user_id: str) -> bool:
        return user_id == "admin"


class MockUserDB(UserDB):
    def findOne(self, id: str) -> User:
        return User(
            _id=id,
            username="user",
            age=25,
            online_status=True,
            vibes=["outgoing"],
            active_mtr=0.5,
            kinky_mtr=0.5,
            location=(0, 0),
        )

    def update(self, user: User):
        pass


class MockMessageDB(MessageDB):
    def findOne(self, message_id: str):
        return Message(
            _id=message_id,
            sender=sender_id,
            reciever=reciever_id,
            text="example",
            time_stamp=datetime.now(),
            photo_id=str(ObjectId()),
        )


class MockStorage(Storage):
    def upload(self, file: bytes, user_id: str, public: bool = False) -> str:
        return "http://example.com/photo123.jpg"

    def download(self, user_id, photo_id) -> bytes:
        return b"mock_photo_data"

    def delete(self, user_id, photo_id):
        pass


def test_upload_photo_admin():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id="admin",
        username="admin",
        age=30,
        online_status=True,
        vibes=["friendly"],
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    photo_use_cases.upload_photo(caller, "user123", b"mock_photo_data")


def test_upload_photo_user():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id="user123",
        username="user",
        age=25,
        online_status=True,
        vibes=["outgoing"],
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    photo_use_cases.upload_photo(caller, "user123", b"mock_photo_data")


def test_upload_photo_unauthorized():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id="other_user",
        username="other",
        age=28,
        online_status=True,
        location=(0, 0),
        vibes=["adventurous"],
        active_mtr=0.5,
        kinky_mtr=0.5,
    )
    with pytest.raises(HTTPException) as exc_info:
        photo_use_cases.upload_photo(caller, "user123", b"mock_photo_data")
    assert exc_info.value.status_code == 403


def test_download_message_photo_admin():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id="admin",
        username="admin",
        age=30,
        online_status=True,
        vibes=["friendly"],
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    photo_use_cases.download_message_photo(caller, "message123")


def test_download_message_photo_sender():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id=sender_id,
        username="sender",
        age=25,
        online_status=True,
        location=(0, 0),
        vibes=["active"],
        active_mtr=0.5,
        kinky_mtr=0.5,
    )
    photo_use_cases.download_message_photo(caller, "message123")


def test_download_message_photo_reciever():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id=reciever_id,
        username="reciever",
        age=27,
        online_status=True,
        vibes=["relaxed"],
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    photo_use_cases.download_message_photo(caller, "message123")


def test_download_message_photo_unauthorized():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id="other_user",
        username="other",
        age=28,
        online_status=True,
        vibes=["adventurous"],
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    with pytest.raises(HTTPException) as exc_info:
        photo_use_cases.download_message_photo(caller, "message123")
    assert exc_info.value.status_code == 403


def test_delete_photo_admin():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id="admin",
        username="admin",
        age=30,
        online_status=True,
        vibes=["friendly"],
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    photo_use_cases.delete_photo(caller, "user123", "photo123")


def test_delete_photo_user():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id="user123",
        username="user",
        age=25,
        online_status=True,
        vibes=["outgoing"],
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    photo_use_cases.delete_photo(caller, "user123", "photo123")


def test_delete_photo_unauthorized():
    photo_use_cases = PhotoUseCases(
        MockAuthDB(), MockUserDB(), MockMessageDB(), MockStorage()
    )
    caller = User(
        _id="other_user",
        username="other",
        age=28,
        online_status=True,
        vibes=["adventurous"],
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    with pytest.raises(HTTPException) as exc_info:
        photo_use_cases.delete_photo(caller, "user123", "photo123")
    assert exc_info.value.status_code == 403
