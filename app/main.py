import logging

import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from schemas.user_schemas import UserBase
from utils.system_config import envs
from utils.auth import get_current_user
from db.database import get_db
from core.log_config import init_loggers
from routers import users, auth


init_loggers()

app = FastAPI()

log = logging.getLogger("app_logger")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app.include_router(users.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup():
    db = get_db()
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    db = get_db()
    await db.disconnect()


@app.get("/")
async def health_check(current_user: UserBase = Depends(get_current_user)):
    log.info("I'm logging")
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working",
        "current_user": current_user
    }


if __name__ == "__main__":

    uvicorn.run("main:app",
                host=envs["HOST"],
                port=envs["PORT"],
                reload=True,
                )
