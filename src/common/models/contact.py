from typing import Annotated
from pydantic import BaseModel, Field


class Contact(BaseModel):
    parties: Annotated[tuple[str, str], Field(kw_only=True)]
    last_message: Annotated[str, Field(kw_only=True)]
