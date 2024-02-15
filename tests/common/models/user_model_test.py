import pytest
from pydantic import ValidationError
import uuid
from src.common.models import User


@pytest.fixture
def sample_user_data():
    return {
        "_id": str(uuid.uuid4()),
        "username": "testuser",
        "age": 25,
        "online_status": True,
        "active_mtr": 0.8,
        "kinky_mtr": None,
        "location": [0, 0],
        "vibes": ["happy", "excited"],
        "photos": [],
        "contacts": [],
        "blocked": [],
    }


def test_create_user(sample_user_data):
    user = User(**sample_user_data)
    assert user.id == sample_user_data["_id"]
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
            _id=str(uuid.uuid4()),
            age=15,
            username="testuser",
            location=(0, 0),
        )


def test_invalid_active_mtr():
    with pytest.raises(ValidationError):
        User(
            _id=str(uuid.uuid4()),
            age=25,
            username="testuser",
            active_mtr=1.5,
            location=(0, 0),
        )


def test_invalid_kinky_mtr():
    with pytest.raises(ValidationError):
        User(
            _id=str(uuid.uuid4()),
            age=25,
            username="testuser",
            kinky_mtr=-0.1,
            location=(0, 0),
        )


def test_empty_location():
    with pytest.raises(ValidationError):
        User(_id=str(uuid.uuid4()), age=25, username="testuser")


def test_default_values():
    user = User(
        _id=str(uuid.uuid4()),
        age=25,
        username="testuser",
        location=(0, 0),
        active_mtr=0.5,
        kinky_mtr=0.5,
    )
    assert not user.online_status
    assert user.vibes == []
    assert user.photos == []
    assert user.blocked == []
