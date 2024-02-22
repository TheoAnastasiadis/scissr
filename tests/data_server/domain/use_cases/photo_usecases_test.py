from datetime import datetime
from unittest.mock import Mock
from src.common.models.message import Message
from src.common.models.user import User
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.data_server.domain.services.db.message import MessageDB
from src.data_server.domain.services.db.user import UserDB
from src.data_server.domain.services.storage.storage import Storage
from src.data_server.domain.use_cases.photos import PhotoUseCases
import pytest
from bson import ObjectId

sender_id = str(ObjectId())
reciever_id = str(ObjectId())
ex_user = User(
    _id=sender_id,
    username="username",
    age=30,
    email="example@email.com",
    online_status=True,
    vibes=["friendly"],
    active_mtr=0.5,
    kinky_mtr=0.5,
    location=(0, 0),
)
ex_caller = APICaller(data_id=sender_id, email=ex_user.email, roles=[])


class MockUserDB(UserDB):
    def findOne(self, id: str) -> User:
        return ex_user

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
    def upload(
        self, file: bytes, user_id: str, photo_id: str, public: bool = False
    ) -> str:
        return "http://example.com/photo123.jpg"

    def download(self, user_id, photo_id) -> bytes:
        return b"mock_photo_data"

    def delete(self, user_id, photo_id):
        pass


@pytest.fixture
def photo_use_cases():
    return PhotoUseCases(
        Mock(spec=MockUserDB()),
        Mock(spec=MockMessageDB()),
        Mock(spec=MockStorage()),
    )


def test_upload_photo(photo_use_cases):
    storage = photo_use_cases.storage_service
    user_db = photo_use_cases.user_db
    photo_use_cases.upload_photo(ex_caller, "photo_id", b"mock_photo_data")
    storage.upload.assert_called_once()
    user_db.findOne.assert_called_once()
    user_db.update.assert_called_once()


def test_download_message_photo_sender(photo_use_cases):
    message_db = photo_use_cases.message_db
    storage = photo_use_cases.storage_service

    message_db.findOne.return_value = MockMessageDB().findOne("message123")
    photo_use_cases.download_message_photo(ex_caller, "message123")

    message_db.findOne.assert_called_once()
    storage.download.assert_called_once()


def test_download_message_photo_reciever(photo_use_cases):
    message_db = photo_use_cases.message_db
    storage = photo_use_cases.storage_service

    message_db.findOne.return_value = MockMessageDB().findOne("message123")
    other_caller = APICaller(
        data_id=reciever_id, email="user2@example.com", roles=[]
    )
    photo_use_cases.download_message_photo(other_caller, "message123")

    message_db.findOne.assert_called_once()
    storage.download.assert_called_once()


def test_delete_photo(photo_use_cases):
    storage = photo_use_cases.storage_service

    photo_use_cases.delete_photo(ex_caller, "photo123")

    storage.delete.assert_called_once()
