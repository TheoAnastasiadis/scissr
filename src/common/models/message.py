from datetime import datetime
from typing import Annotated, Any
from pydantic import BaseModel, Field, AfterValidator, model_validator


class Message(BaseModel):
    id: Annotated[str, Field(alias="_id", kw_only=True), AfterValidator(str)]
    sender: Annotated[str, Field(kw_only=True), AfterValidator(str)]
    reciever: Annotated[str, Field(kw_only=True), AfterValidator(str)]
    text: str | None
    photo_id: str | None
    time_stamp: Annotated[
        datetime, Field(kw_only=True, default_factory=datetime)
    ]

    @model_validator(mode="before")
    @classmethod
    def assert_either_text_or_photo(cls, data: Any) -> Any:
        if isinstance(data, dict):
            assert "text" in data or "photo_id" in data
        return data
