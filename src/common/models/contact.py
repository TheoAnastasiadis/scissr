from typing import Annotated
from pydantic import BaseModel, Field, BeforeValidator
from datetime import datetime


class Contact(BaseModel):
    parties: Annotated[
        tuple[str, str],
        Field(kw_only=True),
        BeforeValidator(lambda pair: [str(el) for el in pair]),
    ]
    last_message: Annotated[str, Field(kw_only=True)]
    time_stamp: Annotated[datetime, Field(kw_only=True)]
