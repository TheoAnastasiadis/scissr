from enum import Enum
from typing import Annotated, NamedTuple, Optional
from pydantic import BaseModel, Field

from src.data_server.domain.use_cases.models.location import LocationTuple


class Operations(str, Enum):
    GE = "ge"
    LE = "le"


class SearchFilters(BaseModel):

    class Kinky_mtr_type(NamedTuple):
        value: Annotated[float, Field(ge=0, le=1, default=0.0)]
        opretation: Annotated[Operations, Field(default=Operations.GE)]

    class Active_mtr_type(NamedTuple):
        value: Annotated[float, Field(ge=0, le=1, default=0.0)]
        opretation: Annotated[Operations, Field(default=Operations.GE)]

    vibes: Annotated[Optional[list[str]], Field(kw_only=True)]
    kinky_mtr: Annotated[
        Optional[dict], Field(default_factory=Kinky_mtr_type, kw_only=True)
    ]
    active_mtr: Annotated[
        Optional[dict], Field(default_factory=Active_mtr_type, kw_only=True)
    ]
    only_active: Annotated[Optional[bool], Field(default=False, kw_only=True)]
    location: Annotated[
        LocationTuple,
        Field(
            kw_only=True,
        ),
    ]
    distance: Annotated[float, Field(default=5, kw_only=True)]
