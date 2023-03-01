from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from databases import Database

from db.database import get_db
from utils.system_config import envs
from utils.hashing import verify_password
from schemas.user_schemas import UserBase, User, UserInDB
from schemas.token import TokenData
from services.logic import UserService


ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return UserBase(
        username=token + "fakedecoded", email="john@example.com"
    )


async def get_current_user(token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)) -> User:
    user_service = UserService(db)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, envs["SECRET_KEY"], algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await user_service.retrieve_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return User(**user.dict())


async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(get_db)):
    user_service = UserService(db=db)

    user = await user_service.retrieve_user(username=form_data.username)
    if not user:
        return False
    if not verify_password(new_pass=form_data.password, old_pass=user.password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, envs["SECRET_KEY"], algorithm=ALGORITHM)
    return encoded_jwt
