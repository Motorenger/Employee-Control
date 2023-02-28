from datetime import datetime

from fastapi import HTTPException

from db.models import users
from utils.hashing import get_password_hash
from schemas.user_schemas import UserCreate, User, UserUpdate


class UserService:
    def __init__(self, db):
        self.db = db
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

    async def get_users(self) -> dict:
        query = self.users.select()
        users = await self.db.fetch_all(query)
        return users

    async def retrieve_user(self, user_id: int) -> User:
        query = self.users.select().where(self.users.c.id == user_id)
        user = await self.db.fetch_one(query)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user)

    async def create_user(self, user: UserCreate) -> User:
        if await self.check_for_existing(email=user.email):
            raise HTTPException(status_code=400, detail="User is not unique.")

        user = user.dict()
        user["password"] = get_password_hash(user["password"])
        user["is_active"] = False
        user["date_joined"] = datetime.now()
        query = self.users.insert()
        await self.db.execute(query=query, values=user)

        query = self.users.select().where(self.users.c.email == user["email"])
        user = await self.db.fetch_one(query=query)
        return User(**user)

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        if not await self.check_for_existing(user_id=user_id):
            raise HTTPException(status_code=404, detail="User not found")

        query = self.users.update().where(self.users.c.id == user_id).values(username=data.username)
        await self.db.execute(query)

        query = self.users.select().where(self.users.c.id == user_id)
        user = await self.db.fetch_one(query)
        return User(**user)

    async def delete_user(self, user_id) -> str:
        if not await self.check_for_existing(user_id=user_id):
            raise HTTPException(status_code=404, detail="User not found")
        query = self.users.delete().where(self.users.c.id == user_id)
        await self.db.execute(query)
        return "User deleted successfully"
