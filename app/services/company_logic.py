from fastapi import HTTPException

from databases import Database

from db.models import companies, invites, requests, users, company_members
from schemas.company_schemas import Company, CompanyBase, CompanyList
from schemas.invite_schemas import InviteData, InviteCreate, Invite, InvitesList
from schemas.request_schemas import RequestData, RequestCreate, RequestList
from schemas.user_schemas import User, UserList
from services.user_logic import UserService


class CompanyService:
    def __init__(self, db: Database, current_user: User | None = None):
        self.db = db
        self.companies = companies
        self.current_user = current_user

    async def check_for_existing(self, comp_name: str | None = None,
                                 company_id: int | None = None,
                                 check_owner: bool = False,
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

        return company

    async def get_companies(self) -> CompanyList:
        query = self.companies.select().where((self.companies.c.visible == True) | (self.companies.c.owner_id == self.current_user.id))
        companies = await self.db.fetch_all(query)
        return CompanyList(companies=companies)

    async def retrieve_company(self, company_id):
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
        update_data = {field:value for field, value in company_data.dict().items() if value is not None}
        
        query = self.companies.update().where(self.companies.c.id == company_id).values(**update_data)
        await self.db.execute(query)

        query = self.companies.select().where(self.companies.c.id == company_id)
        company = await self.db.fetch_one(query)
        return Company(**company)

    async def delete_company(self, company_id: int):
        company = await self.check_for_existing(company_id=company_id)

        query = self.companies.delete().where(self.companies.c.id == company_id)
        await self.db.execute(query)


class CompanyActionsService(CompanyService):
    def __init__(self, current_user: User, db: Database, company_id = None):
        super().__init__(db=db, current_user=current_user)
        self.company_id = company_id
        self.invites = invites
        self.requests = requests
        self.user_service= UserService(db=db, current_user=current_user)
        self.company_members = company_members

    async def get_invites(self) -> InvitesList:
        await self.check_for_existing(company_id=self.company_id)

        query = self.invites.select().where(self.invites.c.company_id == self.company_id)
        invites = await self.db.fetch_all(query=query)
        return InvitesList(invites=invites)

    async def get_members(self) -> UserList:
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = users.select().join(self.company_members).where(self.company_members.c.company_id == self.company_id).where(users.c.id == self.company_members.c.user_id)
        members = await self.db.fetch_all(query=query)
        return UserList(users=members)

    async def send_invite(self, invite_data: InviteData):
        await self.check_for_existing(company_id=self.company_id, check_owner=True)
        if not await self.user_service.check_for_existing(user_id=invite_data.user_id):
            raise HTTPException(status_code=404, detail="Not Found")
        if invite_data.user_id == self.current_user.id:
            raise HTTPException(status_code=404, detail="You can't invite yourself")
        invite_data = invite_data.dict()
        invite_data["company_id"] = self.company_id
        invite = InviteCreate(**invite_data)

        query = self.invites.insert()
        await self.db.execute(query=query, values=invite.dict())

    async def delete_invite(self, invite_id: int):
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = self.invites.delete().where(self.invites.c.id == invite_id)
        await self.db.execute(query)

    async def get_requests(self) -> RequestList:
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = self.requests.select().where(self.requests.c.company_id == self.company_id)
        requests = await self.db.fetch_all(query=query)
        print(requests)
        return RequestList(requests=requests)

    async def send_request(self, request_data: RequestData):
        await self.check_for_existing(company_id=request_data.company_id)
        query = users.select().join(self.company_members).where(self.company_members.c.company_id == request_data.company_id).where(users.c.id == self.current_user.id)
        user = await self.db.fetch_one(query=query)
        if user is not None:
            raise HTTPException(status_code=404, detail="You are already a member")
        request_data = request_data.dict()
        request_data["user_id"] = self.current_user.id
        request = RequestCreate(**request_data)

        query = self.requests.insert()
        await self.db.execute(query=query, values=request.dict())

    async def accept_request(self, request_id: int, response_code=201):
        await self.check_for_existing(company_id=self.company_id, check_owner=True)
        query = self.requests.select().where(self.requests.c.id == request_id)
        request = await self.db.fetch_one(query=query)

        query = self.company_members.insert()
        values = {"user_id": request.user_id, "company_id": request.company_id}

        await self.db.execute(query=query, values=values)

        query = self.requests.delete().where(self.requests.c.id == request_id)
        await self.db.execute(query)

    async def delete_request(self, request_id: int):
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = self.requests.delete().where(self.requests.c.id == request_id)
        await self.db.execute(query)

    async def delete_member(self, user_id: int):
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = self.company_members.delete().where(self.company_members.c.user_id == user_id)
        await self.db.execute(query=query)
