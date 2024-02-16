from src.data_server.domain.services.storage.storage import Storage
import pytest


def test_upload_not_implemented():
    storage = Storage()
    with pytest.raises(NotImplementedError) as exc_info:
        storage.upload(b"test_data", "user1")
    assert str(exc_info.value) == "Storage.upload()"


def test_download_not_implemented():
    storage = Storage()
    with pytest.raises(NotImplementedError) as exc_info:
        storage.download("user1", "photo123")
    assert str(exc_info.value) == "Storage.download()"


def test_delete_not_implemented():
    storage = Storage()
    with pytest.raises(NotImplementedError) as exc_info:
        storage.delete("user1", "photo123")
    assert str(exc_info.value) == "Storage.delete()"
