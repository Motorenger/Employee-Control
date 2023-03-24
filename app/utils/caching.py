import json
from datetime import datetime

def serialize_dates(date):
    print(date.isoformat())
    return date.isoformat()


async def set_cache(records, key: str, redis):
    await redis.set(
        key,
        json.dumps(records, default=serialize_dates),
        ex=48,
    )
