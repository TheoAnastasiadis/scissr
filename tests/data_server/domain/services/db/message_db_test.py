from src.data_server.domain.services.db.message import MessageDB
import pytest


def test_insert_not_implemented():
    db = MessageDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.insert("user1", "user2", "Hello!")
    assert str(exc_info.value) == "MessageDB.inser()"


def test_findOne_not_implemented():
    db = MessageDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.findOne("123")
    assert str(exc_info.value) == "MessageDB.findOne()"


def test_findMany_not_implemented():
    db = MessageDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.findMany(("user1", "user2"))
    assert str(exc_info.value) == "MessageDB.findMany()"
