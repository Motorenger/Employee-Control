from datetime import datetime

from fastapi import HTTPException

from databases import Database

from db.models import users, companies
from utils.hashing import get_password_hash
from schemas.user_schemas import UserCreate, User, UserUpdate, UserList, UserInDB
from schemas.company_schemas import Company, CompanyBase, CompanyList



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
