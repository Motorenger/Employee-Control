from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    visible: bool = True


class Company(CompanyBase):
    id: int
    owner_id: int


class CompanyList(BaseModel):
    companies: list[Company] = []


class CompanyUpdate(BaseModel):
    name: str | None = Field(min_length=1)
    description: str | None = None
    visible: bool | None = None
