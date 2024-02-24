from pydantic import BaseModel
from src.common.models.photo import Photo

from src.common.models.user import PronounsEnum


class PublicUserBody(BaseModel):
    # id from auth db
    uuid: str
    username: str
    pronouns: PronounsEnum
    age: int
    online_status: bool
    active_mtr: float
    kinky_mtr: float
    vibes: list[str] = []
    photos: list[Photo] = []
