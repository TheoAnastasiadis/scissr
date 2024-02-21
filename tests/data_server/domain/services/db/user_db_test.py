from src.common.models.user import User
from src.data_server.domain.services.db.user import UserDB
import pytest


def test_findOne_not_implemented():
    db = UserDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.findOne("123")
    assert str(exc_info.value) == "UserDB.findOne()"


def test_findMany_not_implemented():
    db = UserDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.findMany(
            skip=0,
            limit=20,
            location=(0.0, 0.0),
            distance=10,
            active_mtr={},
            kinky_mtr={},
            exclude_from_results=[],
            excluded_from=[],
            only_active=True,
            vibes=[],
        )
    assert str(exc_info.value) == "UserDB.findMany()"


def test_delete_not_implemented():
    db = UserDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.delete("123")
    assert str(exc_info.value) == "UserDB.delete()"


def test_update_not_implemented():
    db = UserDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.update(
            User(
                _id="123",
                username="example",
                email="example@email.com",
                age=23,
                active_mtr=0.5,
                kinky_mtr=0.5,
                location=(0, 0),
            )
        )
    assert str(exc_info.value) == "UserDB.update()"
