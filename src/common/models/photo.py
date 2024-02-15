from typing import Annotated
from pydantic import BaseModel, Field, AfterValidator


class Photo(BaseModel):
    id: Annotated[str, Field(alias="_id"), AfterValidator(str)]
    url: Annotated[str, Field()]
    public: Annotated[bool, Field(default_factory=lambda: False)]

    class ConfigDict:
        populate_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "url": "/066de609-b04a-4b30-b46c-32537c7f1f6e.jpg",
                "public": True,
            }
        }
