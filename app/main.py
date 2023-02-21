import uvicorn
import aioredis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import system_config
from db.database import db


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
    await db.connect()
    redis = await aioredis.from_url("redis://localhost",  db=1)


@app.on_event("shutdown")
async def shutdown():
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
