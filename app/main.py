import logging
import datetime

import uvicorn

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from utils.system_config import envs
from db.database import get_db
from core.log_config import init_loggers
from routers import users, auth, companies, quizzes


app = FastAPI()

init_loggers()

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
app.include_router(companies.router)
app.include_router(quizzes.router)


@app.on_event("startup")
async def startup():
    db = get_db()
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    db = get_db()
    await db.disconnect()


@app.get("/")
async def health_check():
    log.info("I'm logging")

    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working",
        "result": datetime.datetime.now(),
    }


if __name__ == "__main__":

    uvicorn.run("main:app",
                host=envs["HOST"],
                port=envs["PORT"],
                reload=True,
                lifespan="auto"
                )
