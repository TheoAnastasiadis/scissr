from bson import ObjectId
from src.data_server.impl.services.storage.gcloud_storage import (
    GoogleCloudStorage,
)
import pytest
from google.cloud.storage import Client
from fastapi import HTTPException


@pytest.fixture
def gcstorage():
    # Mocking Google Cloud Storage client and bucket
    client = Client()
    storage = GoogleCloudStorage(client, test=True)
    storage.empty_bucket_for_testing()
    return storage


def test_upload_private(gcstorage):
    file_content = b"test file content"
    user_id = "user1"
    photo_id = "photo1"

    url = gcstorage.upload(file_content, user_id, photo_id)

    assert url is None
    assert gcstorage.private_bucket.blob(f"{user_id}/{photo_id}").exists()


def test_upload_public(gcstorage):
    file_content = b"test file content"
    user_id = "user1"
    photo_id = "photo1"

    url = gcstorage.upload(file_content, user_id, photo_id, public=True)

    assert url is not None
    assert gcstorage.public_bucket.blob(f"{user_id}/{photo_id}").exists()


def test_download_public(gcstorage):
    user_id = "user1"
    photo_id = "photo1"
    expected_content = b"test file content"

    gcstorage.upload(expected_content, user_id, photo_id, public=True)
    content = gcstorage.download(user_id, photo_id)

    assert content == expected_content


def test_download_private(gcstorage):
    user_id = "user1"
    photo_id = "photo1"
    expected_content = b"test file content"

    gcstorage.upload(expected_content, user_id, photo_id, public=False)
    content = gcstorage.download(user_id, photo_id)

    assert content == expected_content


def test_download_not_found(gcstorage):
    user_id = ObjectId()
    photo_id = ObjectId()

    with pytest.raises(HTTPException) as exc_info:
        gcstorage.download(user_id, photo_id)

    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 404


def test_delete_public(gcstorage):
    user_id = "user1"
    photo_id = "photo1"

    gcstorage.upload(b"random file", user_id, photo_id, public=True)
    gcstorage.delete(user_id, photo_id)
    assert not gcstorage.public_bucket.blob(f"{user_id}/{photo_id}").exists()


def test_delete_private(gcstorage):
    user_id = "user1"
    photo_id = "photo1"
    gcstorage.upload(b"random file", user_id, photo_id, public=False)
    gcstorage.delete(user_id, photo_id)
    assert not gcstorage.private_bucket.blob(f"{user_id}/{photo_id}").exists()


def test_delete_not_found(gcstorage):
    user_id = ObjectId()
    photo_id = ObjectId()

    with pytest.raises(HTTPException) as exc_info:
        gcstorage.delete(user_id, photo_id)

    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 404
