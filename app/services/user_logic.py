from datetime import datetime

from fastapi import HTTPException

from databases import Database


from db.models import users, invites, company_members, requests
from utils.hashing import get_password_hash
from schemas.user_schemas import UserCreate, User, UserUpdate, UserList, UserInDB
from schemas.request_schemas import RequestList
from schemas.invite_schemas import InvitesList


class UserService:
    def __init__(self, db: Database, current_user: User | None = None):
        self.db = db
        self.users = users
        self.current_user = current_user

    async def check_for_existing(self, user_id: int = None, email: str = None) -> bool:
        if user_id:
            query = self.users.select().where(self.users.c.id == user_id)
            user = await self.db.fetch_one(query)

            return bool(user)
        elif email:
            query = self.users.select().where(self.users.c.email == email)
            user = await self.db.fetch_one(query)
            return bool(user)

    async def get_users(self) -> UserList:
        query = self.users.select()
        users = await self.db.fetch_all(query)
        return UserList(users=users)

    async def retrieve_user(self, user_id: int = None,
                            username: str = None,
                            email: str = None,
                            password: bool = False
                        ) -> User:
        if user_id:
            query = self.users.select().where(self.users.c.id == user_id)
        elif username:
            query = self.users.select().where(self.users.c.username == username)
        elif email:
            query = self.users.select().where(self.users.c.email == email)
            user = await self.db.fetch_one(query)
            return user

        user = await self.db.fetch_one(query)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if username or password:
            return UserInDB(**user)
        return User(**user)

    async def create_user(self, user: UserCreate) -> User:
        if await self.check_for_existing(email=user.email):
            raise HTTPException(status_code=400, detail="User is not unique.")

        user_dict = user.dict()
        user_dict["password"] = get_password_hash(user.password)
        user_dict["is_active"] = False
        user_dict["date_joined"] = datetime.now()
        user_dict["questions"] = 0
        user_dict["correct"] = 0
        query = self.users.insert()
        await self.db.execute(query=query, values=user_dict)

        query = self.users.select().where(self.users.c.email == user.email)
        user = await self.db.fetch_one(query=query)

        return User(**user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        if not await self.check_for_existing(user_id=user_id):
            raise HTTPException(status_code=404, detail="User not found")
        if user_id != self.current_user.id:
            raise HTTPException(status_code=403, detail="It's not your account")
        query = self.users.update().where(self.users.c.id == user_id).values(username=user_data.username)
        await self.db.execute(query)

        query = self.users.select().where(self.users.c.id == user_id)
        user = await self.db.fetch_one(query)
        return User(**user)

    async def delete_user(self, user_id: int):
        if not await self.check_for_existing(user_id=user_id):
            raise HTTPException(status_code=404, detail="User not found")
        if user_id != self.current_user.id:
            raise HTTPException(status_code=403, detail="It's not your account")

        query = self.users.delete().where(self.users.c.id == user_id)
        await self.db.execute(query)


class UserActionsService(UserService):
    def __init__(self, current_user: User, db: Database):
        super().__init__(db=db, current_user=current_user)
        self.invites = invites
        self.requests = requests
        self.company_members = company_members

    async def get_invites(self) -> InvitesList:
        query = self.invites.select().where(self.current_user.id == self.invites.c.user_id)
        invites = await self.db.fetch_all(query=query)

        return InvitesList(invites=invites)

    async def accept_invite(self, invite_id: int):
        query = self.invites.select().where(self.invites.c.id == invite_id)
        invite = await self.db.fetch_one(query=query)

        query = self.company_members.insert()
        values = {"user_id": invite.user_id, "company_id": invite.company_id,
                  "admin": False, "questions": 0, "correct": 0
                  }

        await self.db.execute(query=query, values=values)

        query = self.invites.delete().where(self.invites.c.id == invite_id)
        await self.db.execute(query)

    async def decline_invite(self, invite_id: int):

        query = self.invites.delete().where(self.invites.c.id == invite_id)
        await self.db.execute(query)

    async def get_requests(self) -> RequestList:
        query = self.requests.select().where(self.requests.c.user_id == self.current_user.id)
        requests = await self.db.fetch_all(query=query)

        return RequestList(requests=requests)

    async def decline_request(self, request_id: int):

        query = self.requests.delete().where(self.requests.c.id == request_id)
        await self.db.execute(query)

    async def leave_company(self, company_id: int):
        query = self.company_members.delete().where(self.company_members.c.user_id == self.current_user.id)
        await self.db.execute(query=query)
