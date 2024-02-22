from fastapi import APIRouter, Depends, UploadFile
from src.common.models.photo import Photo
from src.data_server.domain.services.auth.auth_serivce import AuthService
from data_server.domain.services.db.message import MessageDB
from data_server.domain.services.db.user import UserDB
from data_server.domain.services.storage.storage import Storage

from data_server.domain.use_cases.photos import PhotoUseCases


class PhotosRouter:
    tags = ["photos"]

    photo_use_cases: PhotoUseCases
    auth_service: AuthService

    def __init__(
        self,
        auth_service: AuthService,
        user_db: UserDB,
        message_db: MessageDB,
        storage: Storage,
    ):
        self.photo_use_cases = PhotoUseCases(
            user_db=user_db,
            message_db=message_db,
            storage_service=storage,
        )
        self.auth_service = auth_service

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)
        get_caller = self.auth_service.get_caller

        @router.post("/photo")
        async def upload_photo(
            file: UploadFile, public: bool = False, caller=Depends(get_caller)
        ) -> Photo:
            return self.photo_use_cases.upload_photo(caller, file.file, public)

        @router.get("/photos/message/{message_id}")
        async def get_photo(
            message_id: str, caller=Depends(get_caller)
        ) -> bytes:
            return self.photo_use_cases.download_message_photo(
                caller, message_id
            )

        @router.delete("/photos/{photo_id}")
        async def delete_photo(photo_id: str, caller=Depends(get_caller)):
            return self.photo_use_cases.delete_photo(caller, photo_id)

        return router
