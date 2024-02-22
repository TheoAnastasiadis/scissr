from typing import Optional
from pydantic import BaseModel, Field
from src.common.models.user import PronounsEnum

from src.data_server.domain.use_cases.models.location import LocationTuple


class UpdateUserBody(BaseModel):
    username: Optional[str] = Field(max_length=10, default=None)
    age: Optional[int] = None
    pronouns: Optional[PronounsEnum] = Field(default=None)
    kinky_mtr: Optional[float] = Field(ge=0, le=1, default=None)
    active_mtr: Optional[float] = Field(ge=0, le=1, default=None)
    vibes: list[str] = Field(default=[])
    location: Optional[LocationTuple] = Field(default=None)
