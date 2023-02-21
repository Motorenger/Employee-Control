import uvicorn

import aioredis

from databases import Database

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import system_config
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
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=system_config.HOST, port=system_config.PORT, log_level="info", reload=True)
