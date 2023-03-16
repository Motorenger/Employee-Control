from pydantic import BaseModel


class InviteData(BaseModel):
    user_id: int
    message: str


class InviteCreate(InviteData):
    company_id: int


class Invite(InviteCreate):
    id: int


class InvitesList(BaseModel):
    invites: list[Invite]
