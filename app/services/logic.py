from datetime import datetime

from fastapi import HTTPException

from databases import Database

from db.models import users
from utils.hashing import get_password_hash
from schemas.user_schemas import UserCreate, User, UserUpdate, UserList, UserInDB


class UserService:
    def __init__(self, db: Database, current_user: User | None = None):
        self.db = db
        self.current_user = await current_user.user()
        self.users = users

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

    async def retrieve_user(self, user_id: int = None, username: str = None, email: str = None, password: bool = False) -> User:
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
