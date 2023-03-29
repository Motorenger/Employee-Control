from datetime import datetime
from pydantic import BaseModel


class Notification(BaseModel):
    id: int
    user_id: int
    time: datetime
    message: str
    status: bool


class ListNotification(BaseModel):
    notifications: list[Notification]
