from typing import Optional
from typing_extensions import Annotated
from datetime import datetime
from .photo import Photo
from pydantic import BaseModel, Field, BeforeValidator


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


class User(BaseModel):
    id: Annotated[str, Field(alias="_id"), BeforeValidator(str)]
    username: Annotated[str, Field()]
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
                "username": "Don Quixote",
                "age": 35,
                "online_status": False,
                "active_mtr": 0.5,
                "kinky_mtr": 0.5,
                "location": "#23456",
                "vibes": ["cats"],
                "photos": [Photo.ConfigDict.json_schema_extra["example"]],
                "blocked": [],
            }
        }
