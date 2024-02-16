from src.data_server.domain.services.db.contacts import ContactsDB
import pytest


def test_update_not_implemented():
    db = ContactsDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.update(("user1", "user2"), "Hello!")
    assert str(exc_info.value) == "ContactsDB.update()"


def test_findMany_not_implemented():
    db = ContactsDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.findMany("user1", 0, 10)
    assert str(exc_info.value) == "ContactsDB.findMany()"


def test_remove_not_implemented():
    db = ContactsDB()
    with pytest.raises(NotImplementedError) as exc_info:
        db.remove(("user1", "user2"))
    assert str(exc_info.value) == "ContactsDB.remove()"
