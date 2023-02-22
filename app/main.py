import logging
from logging.config import dictConfig

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from system_config import envs
from db.database import get_db
from core.log_config import app_dict_config, init_loggers


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


@app.on_event("startup")
async def startup():

    db = await anext(get_db())
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    db = await anext(get_db())
    await db.disconnect()


@app.get("/")
async def health_check():
    log.info("I'm logging")


    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working",
    }


if __name__ == "__main__":

    uvicorn.run("main:app",
                host=envs["HOST"],
                port=envs["PORT"],
                reload=True,
                )
