from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    name: str
    description: str | None = None


class Company(CompanyBase):
    visible: bool = True
    owener_id: int
