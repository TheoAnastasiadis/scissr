from typing import Union
from pydantic import BaseModel


class APICaller(BaseModel):
    data_id: Union[str, None]
    email: str
    roles: list[str]


class AuthService:

    def get_caller(self, token: str) -> APICaller:
        raise NotImplementedError("AuthService.get_caller()")
