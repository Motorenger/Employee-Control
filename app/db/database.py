import aioredis

import databases

from databases import Database

from sqlalchemy.ext.declarative import declarative_base

from utils.system_config import envs


Base = declarative_base()


db = Database(envs["DATABASE_URL"])


if envs["ENVIRONMENT"] == "TESTING":
    database = databases.Database(envs["DATABASE_URL_TEST"], force_rollback=True)
else:
    database = databases.Database(envs["DATABASE_URL"])


def get_db() -> databases.Database:
    return database


async def get_redis():
    async with aioredis.from_url(envs["REDIS_URL"],  db=1) as redis:
        return redis
