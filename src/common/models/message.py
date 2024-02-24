from datetime import datetime
from typing import Annotated, Any, Optional
from pydantic import (
    BaseModel,
    Field,
    BeforeValidator,
    AfterValidator,
    model_validator,
)


class Message(BaseModel):
    id: Annotated[
        str,
        Field(alias="_id", kw_only=True),
        AfterValidator(str),
        BeforeValidator(str),
    ]  # this comes from data db as bson ObjectId and needs to be converted
    sender: str = Field(kw_only=True)
    reciever: str = Field(kw_only=True)
    text: Optional[str] = None
    photo_id: Annotated[
        Optional[str], Field(kw_only=True), BeforeValidator(str)
    ] = None  # this comes from data db as bson ObjectId and needs to be converted
    time_stamp: datetime = Field(kw_only=True, default_factory=datetime.now)

    @model_validator(mode="before")
    @classmethod
    def assert_either_text_or_photo(cls, data: Any) -> Any:
        if isinstance(data, dict):
            assert "text" in data or "photo_id" in data
        return data
