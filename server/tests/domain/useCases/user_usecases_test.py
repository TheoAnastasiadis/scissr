import pytest
from unittest.mock import MagicMock
from server.domain.models import User
from server.domain.services.db import UserDB, AuthDB
from server.domain.services.use_cases import UserUseCases

# import pygeohash as pgh

# from pydantic import ValidationError
from fastapi import HTTPException


@pytest.fixture
def user_usecases():
    user_db = MagicMock(spec=UserDB)
    auth_db = MagicMock(spec=AuthDB)
    return UserUseCases(user_db=user_db, auth_db=auth_db)


def test_get_user(user_usecases):
    user_db = user_usecases.user_db
    auth_db = user_usecases.auth_db

    user_id = "123"
    caller = User(
        _id="456",
        username="test_user",
        age=21,
        active_mtr=0.5,
        kinky_mtr=0.5,
        location="#1234",
    )
    user = User(
        _id=user_id,
        username="test_user",
        age=21,
        active_mtr=0.5,
        kinky_mtr=0.5,
        location="#1234",
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
        active_mtr=0.5,
        kinky_mtr=0.5,
        location="#1234",
    )

    user = User(
        _id="345",
        username="test_user",
        age=21,
        active_mtr=0.5,
        kinky_mtr=0.5,
        location="#1234",
    )

    user_db.findOne.return_value = caller
    auth_db.user_is_admin.return_value = False

    # Test successful update
    update_body = {
        "username": "newusername",
        "age": 30,
        "kinky_mtr": 0.4,
        "active_mtr": 0.7,
        "vibes": ["happy", "excited"],
        "lat": 123.456,
        "lon": 789.012,
    }

    user_db.update.return_value = {
        **update_body,
        **caller.model_dump(),
        "_id": caller.id,
    }
    user_usecases.update_user(caller, caller.id, update_body)
    user_db.update.assert_called_with(
        User(**{**caller.model_dump(), **update_body, "_id": caller.id})
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
        active_mtr=0.5,
        kinky_mtr=0.5,
        location="#1234",
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
        active_mtr=0.5,
        kinky_mtr=0.5,
        location="#1234",
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
        active_mtr=0.5,
        kinky_mtr=0.5,
        location="#1234",
    )
    user = User(
        _id=user_id,
        username="test_user",
        age=21,
        active_mtr=0.5,
        kinky_mtr=0.5,
        location="#1234",
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


# def test_get_users(user_usecases):
#     user_db = user_usecases.user_db
#     auth_db = user_usecases.auth_db

#     caller = User(
#         _id="456",
#         username="test_user",
#         age=21,
#         active_mtr=0.5,
#         kinky_mtr=0.5,
#         location="#1234",
#         blocked=["123"],
#     )
#     filters = {
#         "vibes": ["happy", "excited"],
#         "kinky_mtr": {"value": 0.5, "operation": "GE"},
#         "active_mtr": {"value": 0.7, "opretation": "LE"},
#         "only_active": True,
#         "location": (123.456, 789.012),
#     }

#     # Test successful get users
#     user_usecases.get_users(caller, filters)
#     user_db.findMany.assert_called_once_with(
#         0,
#         20,
#         location_hash=pgh.encode(
#             latitude=filters["location"][0], longitude=filters["location"][1]
#         ),
#         filters=filters,
#         exclude_list=["123"],
#     )

#     # Test admin user
#     auth_db.user_is_admin.return_value = True
#     user_usecases.get_users(caller, filters)
#     user_db.findMany.assert_called_with(
#         0, 20, location_hash="s0001z0r7z7k", filters=filters, exclude_list=[]
#     )
