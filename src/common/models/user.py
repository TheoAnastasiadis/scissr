from enum import Enum
from typing import Optional
from typing_extensions import Annotated
from datetime import datetime
from .photo import Photo
from pydantic import BaseModel, Field, BeforeValidator, EmailStr


class Contact(BaseModel):
    id: Annotated[str, Field(alias="_id")]
    last_contacted: Annotated[datetime, Field(default_factory=datetime)]

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "last_contacted": datetime(1998, 6, 23),
            }
        }


class PronounsEnum(str, Enum):
    SHE = "she/her"
    THEY = "they/them"


class User(BaseModel):
    id: Annotated[str, Field(alias="_id"), BeforeValidator(str)]
    username: Annotated[str, Field(max_length=10)]
    email: EmailStr
    pronouns: Annotated[PronounsEnum, Field(default=PronounsEnum.SHE)]
    age: Annotated[int, Field(ge=18, le=100)]
    online_status: Annotated[bool, Field(default_factory=lambda: False)]
    active_mtr: Annotated[Optional[float], Field(ge=0, le=1)]
    kinky_mtr: Annotated[Optional[float], Field(ge=0, le=1)]
    location: Annotated[tuple[float, float], Field()]
    vibes: Annotated[list[str], Field(default_factory=lambda: [])]
    photos: Annotated[list[Photo], Field(default_factory=lambda: [])]
    blocked: Annotated[list[str], Field(default_factory=lambda: [])]

    class ConfigDict:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
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
