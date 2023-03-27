from fastapi import HTTPException

from databases import Database

from services.company_logic import CompanyService
from db.models import companies, invites, requests, users, company_members, records
from schemas.company_schemas import Company, CompanyBase, CompanyList
from schemas.invite_schemas import InviteData, InviteCreate, Invite, InvitesList
from schemas.request_schemas import RequestData, RequestCreate, RequestList
from schemas.records_schemas import Record, RecordsList
from schemas.user_schemas import User, UserList
from services.user_logic import UserService
from utils.caching import get_cache_for_company



class CompanyActionsService(CompanyService):
    def __init__(self, current_user: User, db: Database, company_id = None):
        super().__init__(db=db, current_user=current_user)
        self.company_id = company_id
        self.invites = invites
        self.requests = requests
        self.user_service= UserService(db=db, current_user=current_user)
        self.company_members = company_members
        self.records = records

    async def get_invites(self) -> InvitesList:
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = self.invites.select().where(self.invites.c.company_id == self.company_id)
        invites = await self.db.fetch_all(query=query)
        return InvitesList(invites=invites)

    async def get_members(self) -> UserList:
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = users.select().join(self.company_members).where(
                                                        self.company_members.c.company_id == self.company_id
                                                        ).where(users.c.id == self.company_members.c.user_id)
        members = await self.db.fetch_all(query=query)
        return UserList(users=members)

    async def send_invite(self, invite_data: InviteData):
        if not await self.user_service.check_for_existing(user_id=invite_data.user_id):
            raise HTTPException(status_code=404, detail="This user not found")
        await self.check_for_existing(company_id=self.company_id, check_owner=True)
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
        return RequestList(requests=requests)

    async def send_request(self, request_data: RequestData):
        company = await self.check_for_existing(company_id=request_data.company_id)
        if company.owner_id == self.current_user.id:
            raise HTTPException(status_code=400, detail="User is already a member of the company")
        query = users.select().join(self.company_members).where(self.company_members.c.company_id == request_data.company_id).where(users.c.id == self.current_user.id)
        user = await self.db.fetch_one(query=query)
        if user is not None:
            raise HTTPException(status_code=400, detail="User is already a member of the company")
        request_data = request_data.dict()
        request_data["user_id"] = self.current_user.id
        request = RequestCreate(**request_data)

        query = self.requests.insert()
        await self.db.execute(query=query, values=request.dict())

    async def accept_request(self, request_id: int):
        await self.check_for_existing(company_id=self.company_id, check_owner=True)
        query = self.requests.select().where(self.requests.c.id == request_id)
        request = await self.db.fetch_one(query=query)

        values_d = {"user_id": request.user_id, "company_id": request.company_id, "admin": False}
        query = self.company_members.insert()

        await self.db.execute(query=query, values=values_d)

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

    async def admin(self, user_id: int):
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = self.company_members.update().where(self.company_members.c.user_id == user_id).values({"admin": True})
        await self.db.execute(query)

    async def get_admins(self) -> UserList:
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = users.select().join(self.company_members).where(self.company_members.c.company_id == self.company_id).where(self.company_members.c.admin == True).where(users.c.id == self.company_members.c.user_id)
        admins = await self.db.fetch_all(query=query)
        return UserList(users=admins)

    async def remove_admins(self, user_id: int):
        await self.check_for_existing(company_id=self.company_id, check_owner=True)

        query = self.company_members.update().where(self.company_members.c.user_id == user_id).values({"admin": False})
        await self.db.execute(query)

    async def get_members_records(self, user_id: int | None, quizz_id: int | None, redis):
        await self.check_for_existing(company_id=self.company_id, check_owner_admin=True)

        records_redis = await get_cache_for_company(company_id=self.company_id, user_id=user_id, quizz_id=quizz_id, redis=redis)
        return records_redis

    async def get_analytics_users(self, user_id: int| None) -> RecordsList:
        await self.check_for_existing(company_id=self.company_id, check_owner_admin=True)
        if user_id:
            query = self.records.select().where(
                        self.records.c.company_id == self.company_id, self.records.c.user_id == user_id).order_by(
                        self.records.c.user_id, self.records.c.created_at.desc())
        else: 
            query = self.records.select().where(self.records.c.company_id == self.company_id).order_by(
                                                                            self.records.c.user_id).order_by(
                                                                            self.records.c.created_at.desc()).distinct(
                                                                            self.records.c.user_id)
        analytics = await self.db.fetch_all(query=query)
        return RecordsList(records=analytics)

    async def get_analytics_users_avarages(self) -> RecordsList:
        await self.check_for_existing(company_id=self.company_id, check_owner_admin=True)

        query = self.records.select().where(
                    self.records.c.company_id == self.company_id).order_by(
                    self.records.c.user_id, self.records.c.created_at.desc())

        analytics = await self.db.fetch_all(query=query)
        return RecordsList(records=analytics)
