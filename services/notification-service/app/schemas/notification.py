from pydantic import BaseModel


class NotificationOut(BaseModel):
    id: int
    user_id: int
    order_id: int
    channel: str
    message: str
    status: str

    class Config:
        from_attributes = True
