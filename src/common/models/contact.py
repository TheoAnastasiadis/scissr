from typing import Annotated
from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator
from datetime import datetime


class Contact(BaseModel):
    id: Annotated[
        str, Field(kw_only=True, alias="_id"), BeforeValidator(str)
    ]  # this comes from data db as bson ObjectId and needs to be converted
    parties: tuple[str, str] = Field(kw_only=True)
    last_message: str = Field(kw_only=True)
    time_stamp: datetime = Field(kw_only=True)
