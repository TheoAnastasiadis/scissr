from dataclasses import dataclass, field
from fastapi import APIRouter, UploadFile

tags = ["photos"]


@dataclass
class PhotosRouter:
    data_service: str = field()
    auth_service: str = field()
    router = APIRouter(tags=tags)

    @router.post("/photos/upload")
    async def upload_photo(file: UploadFile):
        pass

    @router.post("/photos/{id}")
    async def update_photo(id: str):
        pass

    @router.delete("/photos/{id}")
    async def delete_photo(id: str):
        pass
