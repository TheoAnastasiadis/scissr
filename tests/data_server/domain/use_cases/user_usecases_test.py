import pytest
from unittest.mock import MagicMock
from src.common.models import User
from src.data_server.domain.services.cache.user_cache import UserCache
from src.data_server.domain.services.db import UserDB, AuthDB, ContactsDB
from src.data_server.domain.use_cases.user import (
    UserUseCases,
    UpdateUserBody,
    Filters,
    LocationTuple,
)

# from pydantic import ValidationError
from fastapi import HTTPException


@pytest.fixture
def user_usecases():
    user_db = MagicMock(spec=UserDB)
    user_cache = MagicMock(spec=UserCache)
    auth_db = MagicMock(spec=AuthDB)
    contacts_db = MagicMock(spec=ContactsDB)
    return UserUseCases(
        user_db=user_db,
        user_cache=user_cache,
        auth_db=auth_db,
        contacts_db=contacts_db,
    )


def test_get_user(user_usecases):
    user_db = user_usecases.user_db
    auth_db = user_usecases.auth_db

    user_id = "123"
    caller = User(
        _id="456",
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    user = User(
        _id=user_id,
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    user_db.findOne.return_value = user
    auth_db.user_is_admin.return_value = False

    # Test successful get user
    assert user_usecases.get_user(caller, user_id) == user
    user_db.findOne.assert_called_once_with(user_id)
    auth_db.user_is_admin.assert_called_once_with(caller.id)

    # Test user not found
    user_db.findOne.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_usecases.get_user(caller, user_id)
    assert exc_info.value.status_code == 404
    assert (
        str(exc_info.value.detail)
        == f"User with id: {user_id} not found on database"
    )

    # Test user blocked caller
    user_db.findOne.return_value = user
    user.blocked = [caller.id]
    with pytest.raises(HTTPException) as exc_info:
        user_usecases.get_user(caller, user_id)
    assert exc_info.value.status_code == 403
    assert str(exc_info.value.detail) == "You cannot view this resource."

    # Test caller blocked caller
    user_db.findOne.return_value = user
    caller.blocked = [user.id]
    with pytest.raises(HTTPException) as exc_info:
        user_usecases.get_user(caller, user_id)
    assert exc_info.value.status_code == 403
    assert str(exc_info.value.detail) == "You cannot view this resource."

    # Test admin user
    caller.blocked = []
    auth_db.user_is_admin.return_value = True
    assert user_usecases.get_user(caller, user_id) == user
    user.blocked = [caller.id]
    assert user_usecases.get_user(caller, user_id) == user


def test_update_user(user_usecases):
    user_db = user_usecases.user_db
    auth_db = user_usecases.auth_db

    user_id = "123"
    caller = User(
        _id="456",
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )

    user = User(
        _id="345",
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )

    user_db.findOne.return_value = caller
    auth_db.user_is_admin.return_value = False

    # Test successful update
    update_body = UpdateUserBody(
        username="newusernam",
        age=30,
        email="example@email.com",
        kinky_mtr=0.4,
        active_mtr=0.7,
        vibes=["happy", "excited"],
        location=LocationTuple(123.456, 789.012),
    )

    user_db.update.return_value = {
        **update_body.model_dump(exclude=["location"]),
        **caller.model_dump(),
        "_id": caller.id,
    }
    user_usecases.update_user(caller, caller.id, update_body)
    user_db.update.assert_called_with(
        User(
            **{
                **caller.model_dump(),
                **update_body.model_dump(exclude=["location"]),
                "_id": caller.id,
            }
        ),
        update_body.location,
    )

    # Test forbidden access due to caller not being admin or owner
    auth_db.user_is_admin.return_value = False
    with pytest.raises(HTTPException) as exc_info:
        user_usecases.update_user(caller, user_id, update_body)
    assert exc_info.value.status_code == 403
    assert str(exc_info.value.detail) == "You cannot perform this action."

    # Test admin has access to all users
    auth_db.user_is_admin.return_value = True
    user_db.findOne.return_value = user
    user_usecases.update_user(caller, user.id, update_body)

    # Test user not found
    user_db.findOne.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_usecases.update_user(caller, caller.id, update_body)
    assert exc_info.value.status_code == 404
    assert (
        str(exc_info.value.detail)
        == f"User with id: {caller.id} not found on database"
    )


def test_block_user(user_usecases):
    user_db = user_usecases.user_db

    user_id = "123"
    caller = User(
        _id="456",
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )

    user_db.findOne.return_value = caller

    # Test successful block
    user_usecases.block_user(caller, user_id)
    user_db.update.assert_called_once_with(caller)


def test_unblock_user(user_usecases):
    user_db = user_usecases.user_db

    user_id = "123"
    caller = User(
        _id="456",
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    caller.blocked = [user_id]

    user_db.findOne.return_value = caller

    # Test successful unblock
    user_usecases.unblock_user(caller, user_id)
    user_db.update.assert_called_once_with(caller)


def test_delete_user(user_usecases):
    user_db = user_usecases.user_db
    auth_db = user_usecases.auth_db

    user_id = "123"
    caller = User(
        _id="456",
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    user = User(
        _id=user_id,
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
    )
    user_db.findOne.return_value = user
    auth_db.user_is_admin.return_value = False

    # Test successful delete
    user_usecases.delete_user(caller, caller.id)
    user_db.delete.assert_called_once_with(user)

    # Test forbidden access due to caller not being admin
    auth_db.user_is_admin.return_value = False
    with pytest.raises(HTTPException) as exc_info:
        user_usecases.delete_user(caller, user.id)
    assert exc_info.value.status_code == 403
    assert str(exc_info.value.detail) == "You cannot perform this action."

    # test allowed for admins
    auth_db.user_is_admin.return_value = True
    user_usecases.delete_user(caller, user.id)


def test_get_users(user_usecases):
    user_db = user_usecases.user_db
    auth_db = user_usecases.auth_db
    user_cache = user_usecases.user_cache

    caller = User(
        _id="456",
        username="test_user",
        age=21,
        email="example@email.com",
        active_mtr=0.5,
        kinky_mtr=0.5,
        location=(0, 0),
        distance=5,
        blocked=["123"],
    )
    filters = Filters(
        vibes=["happy", "excited"],
        kinky_mtr={"value": 0.5, "operation": "GE"},
        active_mtr={"value": 0.7, "operation": "LE"},
        only_active=True,
        location=LocationTuple(123.456, 789.012),
    )

    # Test successful get users
    auth_db.user_is_admin.return_value = False
    user_cache.cache_has.return_value = False
    user_usecases.get_users(caller, filters)
    user_db.findMany.assert_called_with(
        0,
        20,
        location=filters.location,
        distance=5,
        active_mtr=filters.active_mtr["value"],
        active_mtr_op=filters.active_mtr["operation"],
        kinky_mtr=filters.kinky_mtr["value"],
        kinky_mtr_op=filters.kinky_mtr["operation"],
        exclude_from_results=caller.blocked,
        excluded_from=caller.id,
        only_acitve=filters.only_active,
        vibes=filters.vibes,
    )

    # Test admin user
    auth_db.user_is_admin.return_value = True
    user_usecases.get_users(caller, filters)
    user_db.findMany.assert_called_with(
        0,
        20,
        location=filters.location,
        distance=5,
        active_mtr=filters.active_mtr["value"],
        active_mtr_op=filters.active_mtr["operation"],
        kinky_mtr=filters.kinky_mtr["value"],
        kinky_mtr_op=filters.kinky_mtr["operation"],
        exclude_from_results=[],
        excluded_from=None,
        only_acitve=filters.only_active,
        vibes=filters.vibes,
    )
