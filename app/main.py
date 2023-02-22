import uvicorn

import aioredis

from databases import Database

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from system_config import envs
from db.database import get_db, get_redis


app = FastAPI()

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
    # await get_db.connect()
    # await get_redis()
    db = await anext(get_db())
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    db = await anext(get_db())
    await db.disconnect()


@app.get("/")
async def health_check():
    db = await anext(get_db())
    query = "SELECT * FROM users"
    users = await db.fetch_all(query=query)
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working",
    }


if __name__ == "__main__":

    uvicorn.run("main:app", host=envs["HOST"], port=envs["PORT"], log_level="info", reload=True)
