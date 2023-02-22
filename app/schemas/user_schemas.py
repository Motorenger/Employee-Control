from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: int = Field(max_length=8, min_length=8)

    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    username: str | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            "user": {
                "id": 235,
                "username": "Bobpop",
                "email": "ai_bob@email.com",
            }
        }
