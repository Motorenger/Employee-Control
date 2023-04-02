import aioredis

from databases import Database

from utils.system_config import envs



database = Database(envs["DATABASE_URL"])


def get_db() -> Database:
    return database


redis = aioredis.from_url(envs["REDIS_URL"],  db=1)

def get_redis():
    return redis
