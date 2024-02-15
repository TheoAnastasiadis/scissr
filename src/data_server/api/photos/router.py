from fastapi import APIRouter, Request, UploadFile
from src.common.models.photo import Photo
from src.data_server.domain.services.auth import AuthDB
from data_server.domain.services.db.message import MessageDB
from data_server.domain.services.db.user import UserDB
from data_server.domain.services.storage.storage import Storage

from data_server.domain.use_cases.photos import PhotoUseCases


class PhotosRouter:
    tags = ["photos"]

    photo_use_cases: PhotoUseCases

    def __init__(
        self,
        auth_db: AuthDB,
        user_db: UserDB,
        message_db: MessageDB,
        storage: Storage,
    ):
        self.photo_use_cases = PhotoUseCases(
            auth_db=auth_db,
            user_db=user_db,
            message_db=message_db,
            storage_service=storage,
        )

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)

        @router.post("/photos/{user_id}/upload")
        async def upload_photo(
            file: UploadFile,
            user_id: str,
            request: Request,
            public: bool = False,
        ) -> Photo:
            return self.photo_use_cases.upload_photo(
                request.user, user_id, file.file, public
            )

        @router.get("/photos/message/{message_id}")
        async def get_photo(message_id: str, request: Request) -> bytes:
            return self.photo_use_cases.download_message_photo(
                request.user, message_id
            )

        @router.delete("/photos/user/{user_id}/photo/{photo_id}")
        async def delete_photo(photo_id: str, user_id: str, request: Request):
            return self.photo_use_cases.delete_photo(
                request.user, user_id, photo_id
            )

        return router
