from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import HTTPException

from databases import Database

from db.database import get_db
from services.logic import UserService
from utils.hashing import verify_password
from schemas.user_schemas import UserInDB, User


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)):
    user_service = UserService(db)

    user = await user_service.decode_token(token)
    return user


@router.post("/signup")
async def signup(form_data: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(get_db)):
    user_service = UserService(db)

    user = await user_service.login_user(username=form_data.username)
    user = UserInDB(**user)
    if not verify_password(new_pass=form_data.password, old_pass=user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
