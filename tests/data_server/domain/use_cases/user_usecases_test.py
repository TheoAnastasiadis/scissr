from uuid import uuid4
from bson import ObjectId
import pytest
from unittest.mock import MagicMock
from src.common.models import User
from src.common.models.user import PronounsEnum
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.data_server.domain.services.cache.user_cache import UserCache
from src.data_server.domain.services.db import UserDB, ContactsDB
from src.data_server.domain.use_cases.models.location import LocationTuple
from src.data_server.domain.use_cases.models.onboard_body import (
    OnboardUserBody,
)
from src.data_server.domain.use_cases.models.search_filters import (
    SearchFilters,
)
from src.data_server.domain.use_cases.user import (
    UserUseCases,
    UpdateUserBody,
)
from fastapi import HTTPException

ex_caller = APICaller(
    sub=str(uuid4()), email="example@example.com", p_username="example"
)

ex_user = User(
    id=str(ObjectId()),
    uuid=ex_caller.sub,
    email="example@example.com",
    username="example",
    pronouns=PronounsEnum.SHE,
    age=35,
    active_mtr=0.5,
    kinky_mtr=0.5,
    location=(0, 0),
)


@pytest.fixture
def user_usecases():
    user_db = MagicMock(spec=UserDB)
    user_cache = MagicMock(spec=UserCache)
    contacts_db = MagicMock(spec=ContactsDB)
    return UserUseCases(
        user_db=user_db,
        user_cache=user_cache,
        contacts_db=contacts_db,
    )


def test_profile(user_usecases):
    user_db = user_usecases.user_db
    user_db.findOne.return_value = ex_user
    result = user_usecases.profile(ex_caller)
    assert result == ex_user


def test_complete_profile(user_usecases):
    user_db = user_usecases.user_db
    user_db.findOne.return_value = None
    body = OnboardUserBody(
        age=36,
        pronouns=PronounsEnum.SHE,
        kinky_mtr=0.5,
        active_mtr=0.5,
        location=LocationTuple(latitude=0, longitude=0),
    )
    user_usecases.complete_profile(ex_caller, body)
    user_db.insert.assert_called_once()


def test_get_user(user_usecases):
    user_db = user_usecases.user_db
    user_db.findOne.return_value = ex_user

    # Test successful get user
    result = user_usecases.get_user(ex_caller, ex_user.uuid)
    assert result.uuid == ex_user.uuid
    assert result.location
    user_db.findOne.assert_called_once_with(ex_user.uuid)

    # Test user not found
    user_db.findOne.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_usecases.get_user(ex_caller, "user_id")
    assert exc_info.value.status_code == 404
    assert (
        str(exc_info.value.detail)
        == "User with id: user_id not found on database"
    )

    # Test user blocked caller
    user_db.findOne.return_value = User(
        **ex_user.model_dump(exclude={"blocked", "id"}),
        id="user_who_blocked",
        blocked=[ex_caller.sub],
    )
    with pytest.raises(HTTPException) as exc_info:
        user_usecases.get_user(ex_caller, "user_who_blocked")
    assert exc_info.value.status_code == 403
    assert str(exc_info.value.detail) == "You cannot view this resource."


def test_update_user(user_usecases):
    user_db = user_usecases.user_db
    user_db.findOne.return_value = ex_user

    # Test successful update
    update_body = UpdateUserBody(
        username="newusernam",
    )

    user_usecases.update_user(ex_caller, update_body)
    updated_user = User(
        **{
            **ex_user.model_dump(exclude={"id", "username"}),
            "_id": ex_user.id,
            "username": update_body.username,
        }
    )
    user_db.update.assert_called_once_with(updated_user)


def test_block_user(user_usecases):
    user_db = user_usecases.user_db
    contacts_db = user_usecases.contacts_db
    user_db.findOne.return_value = ex_user

    # Test successful block
    user_usecases.block_user(ex_caller, ex_user.id)
    user_db.update.assert_called_once()
    contacts_db.remove.assert_called_once()


def test_unblock_user(user_usecases):
    user_db = user_usecases.user_db
    user_db.findOne.return_value = ex_user

    # Test successful block
    user_usecases.unblock_user(ex_caller, ex_user.id)
    user_db.update.assert_called_once()


def test_get_users(user_usecases):
    user_db = user_usecases.user_db
    user_cache = user_usecases.user_cache

    searchFilters = SearchFilters(
        vibes=["happy", "excited"],
        kinky_mtr={"value": 0.5, "operation": "GE"},
        active_mtr={"value": 0.7, "operation": "LE"},
        only_active=True,
        location=LocationTuple(123.456, 789.012),
        distance=5,
    )

    # Test successful get users
    user_cache.cache_has.return_value = False
    user_db.findOne.return_value = ex_user
    user_usecases.get_users(ex_caller, searchFilters)
    user_db.findMany.assert_called_with(
        0,
        20,
        location=searchFilters.location,
        distance=5.0,
        active_mtr=searchFilters.active_mtr,
        kinky_mtr=searchFilters.kinky_mtr,
        exclude_from_results=[],
        excluded_from=ex_caller.sub,
        only_active=searchFilters.only_active,
        vibes=searchFilters.vibes,
    )
