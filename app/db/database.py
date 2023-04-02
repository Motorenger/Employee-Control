

import aioredis

from databases import Database

from utils.system_config import envs


if envs["ENVIRONMENT"] == "TESTING":
    database = Database(envs["DATABASE_URL_TEST"], force_rollback=True)
else:
    database = Database(envs["DATABASE_URL"])


def get_db() -> Database:
    return database


redis = aioredis.from_url(envs["REDIS_URL"],  db=1)

def get_redis():
    return redis