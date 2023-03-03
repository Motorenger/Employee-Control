from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from utils.auth import authenticate_user, create_access_token, CurrentUser
from schemas.user_schemas import User


token_auth_scheme = HTTPBearer()


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=dict)
async def login(user: User = Depends(authenticate_user)) -> dict:

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token.token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(current_user: User = Depends(CurrentUser)):
    return await current_user.user()
