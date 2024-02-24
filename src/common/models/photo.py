from typing import Annotated, Optional
from pydantic import BaseModel, Field, BeforeValidator


class Photo(BaseModel):
    id: Annotated[
        str, Field(alias="_id", kw_only=True), BeforeValidator(str)
    ]  # this comes from data db as bson ObjectId and needs to be converted
    url: Annotated[str, Field(kw_only=True)]
    public: Optional[bool] = Field(default=False, kw_only=True)

    class ConfigDict:
        populate_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "65d9f4443c86b32b1a821c1b",
                "url": "/65d9f4443c86b32b1a821c1b.jpg",
                "public": True,
            }
        }
