from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt

from databases import Database

from db.database import get_db
from utils.system_config import envs
from utils.hashing import verify_password
from schemas.user_schemas import User, UserCreate, UserSingin
from schemas.token import Token
from services.user_logic import UserService


async def authenticate_user(
    form_data: UserSingin, db: Database = Depends(get_db)
) -> User:
    user_service = UserService(db=db)

    user = await user_service.retrieve_user(email=form_data.email, password=True)
    if not user:
        return False
    if not verify_password(new_pass=form_data.password, old_pass=user.password):
        return False
    return user


def create_access_token(data: dict) -> Token:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, envs["SECRET_KEY"], algorithm=envs["ALGORITHM_AUTH_2"]
    )
    return Token(token=encoded_jwt, token_type="bearer")


auth_scheme = HTTPBearer()


class CurrentUser:
    def __init__(self, token: dict, db: Database):
        self.user_service = UserService(db=db)
        self.token = token.credentials
        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async def get_user_auth2(self) -> User:
        payload = jwt.decode(
            self.token, envs["SECRET_KEY"], algorithms=envs["ALGORITHM_AUTH_2"]
        )
        try:
            email: str = payload.get("sub")
            if email is None:
                raise self.credentials_exception
        except:
            raise self.credentials_exception

        user = await self.user_service.retrieve_user(email=email)
        if user is None:
            raise self.credentials_exception
        return User(**user)

    async def get_user_auth0(self) -> User:
        jwks_client = jwt.PyJWKClient(envs["JWKS_URL"])
        try:
            signing_key = jwks_client.get_signing_key_from_jwt(self.token).key
        except jwt.exceptions.PyJWKClientError:
            raise self.credentials_exception
        except jwt.exceptions.DecodeError:
            raise self.credentials_exception

        try:
            payload = jwt.decode(
                self.token,
                signing_key,
                algorithms=envs["ALGORITHM_AUTH_0"],
                audience=envs["API_AUDIENCE"],
                issuer=envs["ISSUER"],
            )
        except Exception as e:
            raise self.credentials_exception
        try:
            user = await self.user_service.retrieve_user(email=payload["email"])
            if user is None:
                raise Exception
            user = User(**user)
        except:
            user_data = {"email": payload["email"], "password": str(datetime.now())[:8]}
            user = await self.user_service.create_user(user=UserCreate(**user_data))

        return user

    async def user(self) -> User:
        try:
            user = await self.get_user_auth2()
            return user
        except:
            user = await self.get_user_auth0()
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_user(token: dict = Depends(auth_scheme), db: Database = Depends(get_db)):
    current_user = CurrentUser(token=token, db=db)
    user = await current_user.user()
    return user
