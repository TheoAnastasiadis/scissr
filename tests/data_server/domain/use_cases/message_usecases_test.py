from unittest.mock import Mock
from src.common.models.user import User
from src.common.queues.message import MessageQueue
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.data_server.domain.services.db.contacts import ContactsDB
from src.data_server.domain.services.db.message import MessageDB
from src.data_server.domain.services.db.user import UserDB
from src.data_server.domain.use_cases.messages import MessageUseCases
import pytest
from fastapi import HTTPException

ex_caller = APICaller(data_id="id", email="", roles=[])
ex_user = User(
    _id="example",
    username="example",
    age=30,
    email="example@email.com",
    online_status=True,
    location=(0, 0),
    active_mtr=0.5,
    kinky_mtr=0.5,
    vibes=["friendly"],
)


@pytest.fixture
def message_use_cases():
    mock_message_db = Mock(spec=MessageDB)
    mock_queue = Mock(spec=MessageQueue)
    mock_user_db = Mock(spec=UserDB)
    mock_contacts_db = Mock(spec=ContactsDB)
    return MessageUseCases(
        mock_message_db,
        mock_queue,
        mock_user_db,
        mock_contacts_db,
    )


def test_get_messages(message_use_cases):
    message_db = message_use_cases.messages_db

    # test authorized
    message_use_cases.get_messages(ex_caller, (ex_caller.data_id, "other_id"))
    message_db.findMany.assert_called_once()


def test_get_messages_unauthorized(message_use_cases):
    user_db = message_use_cases.user_db
    reciever = User(
        _id="rec1234",
        username="caller",
        age=25,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["confident"],
        blocked=[],
    )
    user_db.findOne.return_value = reciever
    # test unauthorized
    with pytest.raises(HTTPException) as exc_info:
        message_use_cases.get_messages(ex_caller, ("random_id", "other_id"))
    assert exc_info.value.status_code == 403


def test_send_message_blocked(message_use_cases):
    user_db = message_use_cases.user_db
    reciever = User(
        _id="rec1234",
        username="caller",
        age=25,
        email="example@email.com",
        online_status=True,
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
        vibes=["confident"],
        blocked=[ex_caller.data_id],
    )

    user_db.findOne.return_value = reciever
    with pytest.raises(HTTPException) as exc_info:
        message_use_cases.send_message(ex_caller, reciever.id, "Hello!")
    assert exc_info.value.status_code == 403


def test_send_message_empty_input(message_use_cases):
    user_db = message_use_cases.user_db

    user_db.findOne.return_value = ex_user
    with pytest.raises(HTTPException) as exc_info:
        message_use_cases.send_message(ex_caller, "rec1234")
    assert exc_info.value.status_code == 400


def test_send_message_text(message_use_cases):
    queue = message_use_cases.message_queue
    contacts_db = message_use_cases.contacts_db
    user_db = message_use_cases.user_db

    user_db.findOne.return_value = ex_user
    message_use_cases.send_message(ex_caller, "rec1234", "Hello!")

    queue.announce.assert_called_once()
    contacts_db.update.assert_called_once()


def test_send_message_photo(message_use_cases):
    queue = message_use_cases.message_queue
    contacts_db = message_use_cases.contacts_db
    user_db = message_use_cases.user_db

    user_db.findOne.return_value = ex_user
    message_use_cases.send_message(ex_caller, "rec1234", photo_id="Hello!")

    queue.announce.assert_called_once()
    contacts_db.update.assert_called_once()
