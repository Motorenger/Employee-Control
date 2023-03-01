from pydantic import BaseModel


class Token(BaseModel):
    token: str


class TokenData(BaseModel):
    username: str | None = None


