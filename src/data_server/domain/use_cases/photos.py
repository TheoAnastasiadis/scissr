from bson import ObjectId
from src.common.models.photo import Photo
from src.common.models.user import User
from data_server.domain.services.db.auth import AuthDB
from data_server.domain.services.db.message import MessageDB
from data_server.domain.services.db.user import UserDB
from data_server.domain.services.storage.storage import Storage
from fastapi import HTTPException
from pydantic import validate_call


class PhotoUseCases:

    auth_db: AuthDB
    storage_service: Storage
    user_db: UserDB
    message_db: MessageDB

    def __init__(
        self,
        auth_db: AuthDB,
        user_db: UserDB,
        message_db: MessageDB,
        storage_service: Storage,
    ):
        self.auth_db = auth_db
        self.storage_service = storage_service
        self.user_db = user_db
        self.message_db = message_db

    @validate_call
    def upload_photo(
        self, caller: User, user_id: str, file: bytes, public: bool = False
    ) -> Photo:
        is_admin = self.auth_db.user_is_admin(caller.id)

        if not is_admin and caller.id != user_id:
            raise HTTPException(
                status_code=403, detail="You cannot perform this action"
            )

        # business.validate_upload(user_id)
        url = self.storage_service.upload(file, user_id, public)
        # business.assess_upload(url)
        photo_id = ObjectId()
        if not public:
            url = f"/:private:/{user_id}/{photo_id}"

        user = self.user_db.findOne(user_id)
        user.photos.append(Photo(_id=photo_id, url=url, public=public))
        self.user_db.update(user)

    @validate_call
    def download_message_photo(self, caller: User, message_id: str) -> bytes:
        is_admin = self.auth_db.user_is_admin(caller.id)

        message = self.message_db.findOne(message_id)
        if not is_admin and caller.id not in [
            message.sender.id,
            message.reciever.id,
        ]:
            raise HTTPException(
                status_code=403, detail="You cannot view this resource"
            )

        if "photo" not in message:
            raise HTTPException(
                status_code=404, detail="Message does not contain image"
            )

        return self.storage_service.download(
            message.sender.id, message.photo.id
        )

    @validate_call
    def delete_photo(self, caller: User, user_id: str, photo_id: str):
        is_admin = self.auth_db.user_is_admin(caller.id)

        if not is_admin and caller.id != user_id:
            raise HTTPException(
                status_code=403, detail="You cannot perform this action"
            )

        self.storage_service.delete(user_id, photo_id)
