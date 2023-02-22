import aioredis

from databases import Database

from sqlalchemy.ext.declarative import declarative_base

from system_config import envs


Base = declarative_base()


db = Database(envs["DATABASE_URL"])

def get_db():
    return db


async def get_redis():
    async with aioredis.from_url(envs["REDIS_URL"],  db=1) as redis:
        return redis
