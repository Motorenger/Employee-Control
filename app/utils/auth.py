from schemas.user_schemas import UserBase

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token):
    return UserBase(
        username=token + "fakedecoded", email="john@example.com"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user