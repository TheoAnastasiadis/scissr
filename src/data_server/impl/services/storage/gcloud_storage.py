from fastapi import HTTPException
from src.common.config import config
from src.data_server.domain.services.storage.storage import Storage
from google.cloud import storage


class GoogleCloudStorage(Storage):

    _public_bucket_name = config["PUBLIC_GCP_BUCKET"]
    _private_bucket_name = config["PRIVATE_GCP_BUCKET"]

    def __init__(self, client: storage.Client):
        self.client = client
        self.public_bucket = self.client.bucket(self._public_bucket_name)
        self.private_bucket = self.client.bucket(self._private_bucket_name)

    def upload(
        self, file: bytes, user_id: str, photo_id: str, public: bool = False
    ) -> str | None:
        blob_name = f"{user_id}/{photo_id}"
        if public:
            blob = self.public_bucket.blob(blob_name)
            blob.upload_from_string(file)
            blob.make_public()
            return blob.public_url()
        else:
            blob = self.private_bucket.blob(blob_name)
            blob.upload_from_string(file)
            return None

    def download(self, user_id, photo_id) -> bytes:
        blob_name = f"{user_id}/{photo_id}"
        if self.public_bucket.blob(blob_name).exists():
            return self.public_bucket.blob(blob_name).download_as_string()
        elif self.private_bucket.blob(blob_name).exists():
            return self.private_bucket.blob(blob_name).download_as_string()
        else:
            raise HTTPException(status_code=404, detail="File Not Found")

    def delete(self, user_id, photo_id):
        blob_name = f"{user_id}/{photo_id}"
        if self.public_bucket.blob(blob_name).exists():
            self.public_bucket.blob(blob_name).delete()
        elif self.private_bucket.blob(blob_name).exists():
            self.private_bucket.blob(blob_name).delete()
        else:
            raise HTTPException(status_code=404, detail="File Not Found")
