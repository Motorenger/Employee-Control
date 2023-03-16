from pydantic import BaseModel


class RequestData(BaseModel):
    company_id: int
    message: str


class RequestCreate(RequestData):
    user_id: int


class Request(RequestCreate):
    id: int


class RequestList(BaseModel):
    requests: list[Request]
