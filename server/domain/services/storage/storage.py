class Storage:

    def upload(self, file: bytes, user_id: str, public: bool = False) -> str:
        raise NotImplementedError("Storage.upload()")

    def download(self, user_id, photo_id) -> bytes:
        raise NotImplementedError("Storage.download()")

    def delete(self, user_id, photo_id):
        raise NotImplementedError("Storage.delete()")
