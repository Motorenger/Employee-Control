from fastapi import HTTPException

from databases import Database

from db.models import companies, invites, requests, users, company_members, quizzes
from schemas.company_schemas import Company, CompanyBase, CompanyList
from schemas.quizz_schemas import QuizzList
from schemas.invite_schemas import InviteData, InviteCreate, Invite, InvitesList
from schemas.request_schemas import RequestData, RequestCreate, RequestList
from schemas.user_schemas import User, UserList
from services.user_logic import UserService


class CompanyService:
    def __init__(self, db: Database, current_user: User | None = None):
        self.db = db
        self.companies = companies
        self.current_user = current_user
        self.company_members = company_members
        self.quizzes = quizzes


    async def check_for_existing(self, comp_name: str | None = None,
                                 company_id: int | None = None,
                                 check_owner: bool = False,
                                 check_owner_admin: bool = False,
                                 check_member: bool = False,
                                 exeptions: bool = True
                                 ):
        if comp_name:
            query = self.companies.select().where(self.companies.c.name == comp_name)
        elif company_id:
            query = self.companies.select().where(self.companies.c.id == company_id)
        company = await self.db.fetch_one(query=query)
        if not exeptions:
            return company
        if company is None:
            raise HTTPException(status_code=404, detail="Not Found")
        if check_owner:
            if company.owner_id != self.current_user.id:
                raise HTTPException(status_code=403, detail="It is not your company")
        if check_owner_admin:
            admin = await self.db.fetch_one(query=self.company_members.select().where(self.company_members.c.user_id == self.current_user.id).where(self.company_members.c.admin == True))
            if company.owner_id != self.current_user.id and admin is None:
                raise HTTPException(status_code=403, detail="You is not allowed")
        if check_member:
            member = await self.db.fetch_one(query=self.company_members.select().where(self.company_members.c.user_id == self.current_user.id))
            if member is None:
                raise HTTPException(status_code=403, detail="You are not allowed")
        return company

    async def get_companies(self) -> CompanyList:
        query = self.companies.select().where((self.companies.c.visible == True) | (self.companies.c.owner_id == self.current_user.id))
        companies = await self.db.fetch_all(query)
        return CompanyList(companies=companies)

    async def retrieve_company(self, company_id: int) -> Company:
        company = await self.check_for_existing(company_id=company_id, check_owner=True)

        return Company(**company)

    async def create_company(self, company: CompanyBase) -> Company:
        if await self.check_for_existing(comp_name=company.name, exeptions=False) is not None:
            raise HTTPException(status_code=400, detail="Such company name already exists")
        company_dict = company.dict()
        company_dict["owner_id"] = self.current_user.id
        query = self.companies.insert()
        await self.db.execute(query=query, values=company_dict)

        query = self.companies.select().where(self.companies.c.name == company.name)
        company = await self.db.fetch_one(query=query)
        return Company(**company)

    async def update_company(self, company_id: int, company_data: str) -> Company:
        company = Company(**await self.check_for_existing(company_id=company_id, check_owner=True))
        update_data = {field: value for field, value in company_data.dict().items() if value is not None}

        query = self.companies.update().where(self.companies.c.id == company_id).values(**update_data)
        await self.db.execute(query)

        query = self.companies.select().where(self.companies.c.id == company_id)
        company = await self.db.fetch_one(query)
        return Company(**company)

    async def delete_company(self, company_id: int):
        await self.check_for_existing(company_id=company_id)

        query = self.companies.delete().where(self.companies.c.id == company_id)
        await self.db.execute(query)

    async def list_quizzes(self, company_id: int) -> QuizzList:
        query = self.quizzes.select().where(self.quizzes.c.company_id == company_id)
        quizzes = await self.db.fetch_all(query=query)

        return QuizzList(quizzes=quizzes)
