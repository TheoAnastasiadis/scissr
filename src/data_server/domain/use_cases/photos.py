from bson import ObjectId
from src.common.models.photo import Photo
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.data_server.domain.services.db.message import MessageDB
from src.data_server.domain.services.db.user import UserDB
from src.data_server.domain.services.storage.storage import Storage
from fastapi import HTTPException
from pydantic import validate_call


class PhotoUseCases:

    storage_service: Storage
    user_db: UserDB
    message_db: MessageDB

    def __init__(
        self,
        user_db: UserDB,
        message_db: MessageDB,
        storage_service: Storage,
    ):
        self.storage_service = storage_service
        self.user_db = user_db
        self.message_db = message_db

    @validate_call
    def upload_photo(
        self,
        caller: APICaller,
        photo_id: str,
        file: bytes,
        public: bool = False,
    ) -> Photo:

        # business.validate_upload(user_id)
        photo_id = str(ObjectId())
        url = self.storage_service.upload(
            file, caller.data_id, photo_id, public
        )
        # business.assess_upload(url)
        if not public:
            url = f"/:private:/{caller.data_id}/{photo_id}"

        user = self.user_db.findOne(caller.data_id)
        user.photos.append(Photo(_id=photo_id, url=url, public=public))
        self.user_db.update(user)

    @validate_call
    def download_message_photo(
        self, caller: APICaller, message_id: str
    ) -> bytes:

        message = self.message_db.findOne(message_id)
        if caller.data_id not in [
            message.sender,
            message.reciever,
        ]:
            raise HTTPException(
                status_code=403, detail="You cannot view this resource"
            )

        if not message.photo_id:
            raise HTTPException(
                status_code=404, detail="Message does not contain image"
            )

        return self.storage_service.download(message.sender, message.photo_id)

    @validate_call
    def delete_photo(self, caller: APICaller, photo_id: str):

        self.storage_service.delete(caller.data_id, photo_id)
