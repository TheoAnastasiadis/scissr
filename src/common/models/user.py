from enum import Enum
from typing import Annotated
from uuid import uuid4
from bson import ObjectId
from .photo import Photo
from pydantic import (
    BaseModel,
    BeforeValidator,
    EmailStr,
    Field,
)


class PronounsEnum(str, Enum):
    SHE = "she/her"
    THEY = "they/them"


class User(BaseModel):
    # id from data db
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(ObjectId()), kw_only=True, alias="_id"
        ),
        BeforeValidator(str),
    ]
    # id from auth db
    uuid: str = Field(default_factory=lambda: str(uuid4()), kw_only=True)
    username: str = Field(max_length=10, kw_only=True)
    email: EmailStr = Field(kw_only=True)
    pronouns: PronounsEnum = Field(default=PronounsEnum.SHE, kw_only=True)
    age: int = Field(ge=18, le=100, kw_only=True)
    online_status: bool = Field(default=False, kw_only=True)
    active_mtr: float = Field(ge=0, le=1, kw_only=True)
    kinky_mtr: float = Field(ge=0, le=1, kw_only=True)
    location: tuple[float, float] = Field(kw_only=True)
    vibes: list[str] = Field(default=[], kw_only=True)
    photos: list[Photo] = Field(default=[], kw_only=True)
    blocked: list[str] = Field(default=[], kw_only=True)

    class ConfigDict:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "ObjectId(65d9f3463c86b32b1a821c1a)",
                "uuid": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "username": "don_quixot",
                "email": "email@example.com",
                "pronouns": "she/her",
                "age": 35,
                "online_status": False,
                "active_mtr": 0.5,
                "kinky_mtr": 0.5,
                "location": (23.34567, 37.23456),
                "vibes": ["cats"],
                "photos": [Photo.ConfigDict.json_schema_extra["example"]],
                "blocked": [],
            }
        }
