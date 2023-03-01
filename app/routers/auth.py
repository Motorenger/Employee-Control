from fastapi import APIRouter, Depends
from fastapi import HTTPException

from databases import Database

from db.database import get_db
from services.logic import UserService
from utils.hashing import verify_password
from utils.auth import get_current_user, authenticate_user, create_access_token
from schemas.user_schemas import UserInDB, User


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
async def login(user: User = Depends(authenticate_user)):

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
