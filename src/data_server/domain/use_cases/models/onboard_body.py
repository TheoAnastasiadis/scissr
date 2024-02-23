from pydantic import BaseModel, Field

from src.common.models.user import PronounsEnum
from src.data_server.domain.use_cases.models.location import LocationTuple


class OnboardUserBody(BaseModel):
    age: int = Field(ge=18)
    pronouns: PronounsEnum
    kinky_mtr: float = Field(ge=0, le=1)
    active_mtr: float = Field(ge=0, le=1)
    vibes: list[str] = Field(default=[])
    location: LocationTuple
