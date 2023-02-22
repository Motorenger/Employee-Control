import aioredis

from databases import Database

import system_config


async def get_db():
    async with Database(system_config.DATABASE_URL) as db:
        return db


async def get_redis():
    async with aioredis.from_url(system_config.REDIS_URL,  db=1) as redis:
        yield redis
