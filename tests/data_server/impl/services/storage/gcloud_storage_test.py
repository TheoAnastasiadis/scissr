import pytest
from unittest.mock import MagicMock
from google.cloud import storage
from fastapi import HTTPException
from src.data_server.impl.services.storage.gcloud_storage import (
    GoogleCloudStorage,
)


@pytest.fixture
def gcs_client():
    return MagicMock(spec=storage.Client)


@pytest.fixture
def google_cloud_storage(gcs_client):
    return GoogleCloudStorage(gcs_client)


def test_upload_public(google_cloud_storage):
    file = b"test_content"
    user_id = "user123"
    photo_id = "photo123"
    google_cloud_storage.public_bucket.blob.return_value = blob = MagicMock()
    blob.public_url = "https://example.com"
    assert (
        google_cloud_storage.upload(file, user_id, photo_id, public=True)
        == "https://example.com"
    )
    blob.upload_from_string.assert_called_once_with(file)
    blob.make_public.assert_called_once()


def test_upload_private(google_cloud_storage):
    file = b"test_content"
    user_id = "user123"
    photo_id = "photo123"
    assert (
        google_cloud_storage.upload(file, user_id, photo_id, public=False)
        == None
    )
    google_cloud_storage.private_bucket.blob.assert_called_once_with(
        f"{user_id}/{photo_id}"
    )
    google_cloud_storage.private_bucket.blob.return_value.upload_from_string.assert_called_once_with(
        file
    )


def test_download_public(google_cloud_storage):
    user_id = "user123"
    photo_id = "photo123"
    google_cloud_storage.public_bucket.blob.return_value.exists.return_value = (
        True
    )
    google_cloud_storage.public_bucket.blob.return_value.download_as_string.return_value = (
        b"test_content"
    )
    assert google_cloud_storage.download(user_id, photo_id) == b"test_content"


def test_download_private(google_cloud_storage):
    user_id = "user123"
    photo_id = "photo123"
    google_cloud_storage.public_bucket.blob.return_value.exists.return_value = (
        False
    )
    google_cloud_storage.private_bucket.blob.return_value.exists.return_value = (
        True
    )
    google_cloud_storage.private_bucket.blob.return_value.download_as_string.return_value = (
        b"test_content"
    )
    assert google_cloud_storage.download(user_id, photo_id) == b"test_content"


def test_download_not_found(google_cloud_storage):
    user_id = "user123"
    photo_id = "photo123"
    google_cloud_storage.public_bucket.blob.return_value.exists.return_value = (
        False
    )
    google_cloud_storage.private_bucket.blob.return_value.exists.return_value = (
        False
    )
    with pytest.raises(HTTPException):
        google_cloud_storage.download(user_id, photo_id)


def test_delete_public(google_cloud_storage):
    user_id = "user123"
    photo_id = "photo123"
    google_cloud_storage.public_bucket.blob.return_value.exists.return_value = (
        True
    )
    google_cloud_storage.delete(user_id, photo_id)
    google_cloud_storage.public_bucket.blob.return_value.delete.assert_called_once()


def test_delete_private(google_cloud_storage):
    user_id = "user123"
    photo_id = "photo123"
    google_cloud_storage.public_bucket.blob.return_value.exists.return_value = (
        False
    )
    google_cloud_storage.private_bucket.blob.return_value.exists.return_value = (
        True
    )
    google_cloud_storage.delete(user_id, photo_id)
    google_cloud_storage.private_bucket.blob.return_value.delete.assert_called_once()


def test_delete_not_found(google_cloud_storage):
    user_id = "user123"
    photo_id = "photo123"
    google_cloud_storage.public_bucket.blob.return_value.exists.return_value = (
        False
    )
    google_cloud_storage.private_bucket.blob.return_value.exists.return_value = (
        False
    )
    with pytest.raises(HTTPException):
        google_cloud_storage.delete(user_id, photo_id)
