from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from utils.auth import authenticate_user, create_access_token, CurrentUser
from schemas.user_schemas import User
from schemas.token import Token


token_auth_scheme = HTTPBearer()


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=Token)
async def login(user: User = Depends(authenticate_user)) -> Token:

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.email})
    return access_token


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(CurrentUser)) -> User:
    return await current_user.user()
