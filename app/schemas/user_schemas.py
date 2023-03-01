import datetime

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None


class UserCreate(UserBase):
    password: str = Field(max_length=8, min_length=8)

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str


class User(UserBase):
    id: int
    is_active: bool | None = None
    date_joined: datetime.datetime | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            "user": {
                "id": 235,
                "username": "Bobpop",
                "email": "ai_bob@email.com",
                "is_active": "True",
                "date_joined": "time",
            }
        }


class UserList(BaseModel):
    users: list[User] = []
