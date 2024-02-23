from pydantic import BaseModel


class APICaller(BaseModel):
    sub: str
    email: str
    p_username: str


class AuthService:

    def get_caller(self, token: str) -> APICaller:
        raise NotImplementedError("AuthService.get_caller()")
