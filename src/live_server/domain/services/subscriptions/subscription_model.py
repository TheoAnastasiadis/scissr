from pydantic import BaseModel, Field


class Subscription(BaseModel):
    id: str = Field(alias="_id")
    user_uuid: str
    endpoint: str
    auth: str
    p256dh: str
