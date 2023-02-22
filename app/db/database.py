import aioredis

from databases import Database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from system_config import envs


engine = create_engine(envs["DATABASE_URL"])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    async with Database(system_config.DATABASE_URL) as db:
        return db


async def get_redis():
    async with aioredis.from_url(envs["REDIS_URL"],  db=1) as redis:
        yield redis
