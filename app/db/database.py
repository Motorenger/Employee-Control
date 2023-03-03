import aioredis

from databases import Database

from utils.system_config import envs


db = Database(envs["DATABASE_URL"])


if envs["ENVIRONMENT"] == "TESTING":
    database = Database(envs["DATABASE_URL_TEST"], force_rollback=True)
else:
    database = Database(envs["DATABASE_URL"])


def get_db() -> Database:
    return database


async def get_redis():
    async with aioredis.from_url(envs["REDIS_URL"],  db=1) as redis:
        return redis
