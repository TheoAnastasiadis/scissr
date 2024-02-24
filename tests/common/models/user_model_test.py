from bson import ObjectId
import pytest
from pydantic import ValidationError
from uuid import uuid4
from src.common.models import User


@pytest.fixture
def sample_user_data():
    return {
        "id": ObjectId(),
        "uuid": str(uuid4()),
        "username": "testuser",
        "email": "test@email.com",
        "pronouns": "she/her",
        "age": 25,
        "online_status": True,
        "active_mtr": 0.5,
        "kinky_mtr": 0.5,
        "location": [0, 0],
        "vibes": ["happy", "excited"],
        "photos": [],
        "contacts": [],
        "blocked": [],
    }


def test_create_user(sample_user_data):
    user = User(**sample_user_data)
    assert user.username == sample_user_data["username"]
    assert user.age == sample_user_data["age"]
    assert user.online_status == sample_user_data["online_status"]
    assert user.active_mtr == sample_user_data["active_mtr"]
    assert user.kinky_mtr == sample_user_data["kinky_mtr"]
    assert user.location == tuple(sample_user_data["location"])
    assert user.vibes == sample_user_data["vibes"]
    assert user.photos == sample_user_data["photos"]
    assert user.blocked == sample_user_data["blocked"]


def test_invalid_age():
    with pytest.raises(ValidationError):
        User(
            id=str(ObjectId()),
            uuid=str(uuid4()),
            age=15,
            email="test@example.com",
            username="testuser",
            kinky_mtr=0.5,
            active_mtr=0.5,
            location=(0, 0),
        )


def test_invalid_active_mtr():
    with pytest.raises(ValidationError):
        User(
            id=str(ObjectId()),
            uuid=str(uuid4()),
            age=25,
            username="testuser",
            email="test@example.com",
            active_mtr=1.5,
            kinky_mtr=0.5,
            location=(0, 0),
        )


def test_invalid_kinky_mtr():
    with pytest.raises(ValidationError):
        User(
            id=str(ObjectId()),
            uuid=str(uuid4()),
            age=25,
            username="testuser",
            email="test@example.com",
            active_mtr=0.5,
            kinky_mtr=-0.1,
            location=(0, 0),
        )


def test_default_values():
    user = User(
        id=str(ObjectId()),
        uuid=str(uuid4()),
        age=25,
        username="testuser",
        email="test@example.com",
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
    )
    assert not user.online_status
    assert user.vibes == []
    assert user.photos == []
    assert user.blocked == []
