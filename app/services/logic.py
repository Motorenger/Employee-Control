from datetime import datetime

from fastapi import HTTPException

from utils.hashing import get_password_hash
from schemas.user_schemas import UserInDB


class UserService:
    def __init__(self, db):
        self.db = db

    async def check_for_existing(self, user_id: int = None, email: str = None):
        if user_id:
            query = "SELECT * FROM users WHERE id = :id"
            user = await self.db.fetch_one(query, values={"id": user_id})
            return bool(user)
        elif email:
            query = "SELECT * FROM users WHERE email = :email"
            user = await self.db.fetch_one(query, values={"email": email})
            return bool(user)

    async def get_users(self) -> dict:
        query = "SELECT * FROM users"
        users = await self.db.fetch_all(query)
        return users

    async def retrieve_user(self, user_id: int) -> dict:

        query = "SELECT * FROM users WHERE id = :id"
        user = await self.db.fetch_one(query, values={"id": user_id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create_user(self, user: dict) -> dict:
        if await self.check_for_existing(email=user.email):
            raise HTTPException(status_code=400, detail="User is not unique.")
        user = user.dict()
        user["password"] = get_password_hash(user["password"])
        user["is_active"] = False
        user["date_joined"] = datetime.now()
        query = """INSERT INTO users(email, username, password, is_active, date_joined)
                    VALUES (:email, :username, :password, :is_active, :date_joined)
                """
        await self.db.execute(query=query, values=user)

        users = await self.db.fetch_all(query="SELECT * FROM users")
        return users[-1]

    async def update_user(self, user_id: int, data: dict) -> dict:
        if not await self.check_for_existing(user_id=user_id):
            raise HTTPException(status_code=404, detail="User not found")
        query = """UPDATE users
                   SET username = :username
                   WHERE id = :id;
                """
        data["id"] = user_id
        await self.db.execute(query, values=data)
        query = "SELECT * FROM users WHERE id = :id"
        user = await self.db.fetch_one(query, values={"id": user_id})
        return user

    async def delete_user(self, user_id):
        if not await self.check_for_existing(user_id=user_id):
            raise HTTPException(status_code=404, detail="User not found")
        query = "DELETE FROM users WHERE id = :id"
        await self.db.execute(query, values={"id": user_id})

    async def login_user(self, username):
        query = "SELECT * FROM users WHERE username = :username"
        user = await self.db.fetch_one(query, values={"username": username})
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return user

    async def decode_token(self, token):
        query = "SELECT * FROM users WHERE username = :username"
        user = await self.db.fetch_one(query, values={"username": token})
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserInDB(**user)
