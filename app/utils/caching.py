import json
import datetime


def serialize_dates(date):
    return date.isoformat()


async def set_cache(records, key: str, redis):
    await redis.set(
        key,
        json.dumps(records, default=serialize_dates),
        ex=datetime.timedelta(days=2),
    )


def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, str) and v.endswith('+00:00'):
            try:
                dct[k] = datetime.datetime.fromisoformat(v)
            except:
                pass
    return dct


async def get_cache_for_user(user_id: int, redis):
    keys = await redis.scan(match=f"{user_id}_*")
    records = await redis.mget(keys[1])

    if records:
        return [json.loads(record, object_hook=datetime_parser) for record in records]


async def get_cache_for_company(company_id: int, user_id: int | None, quizz_id: int | None, redis):
    if user_id is not None:
        keys = await redis.scan(match=f"{user_id}_*_{company_id}")
    elif quizz_id is not None:
        keys = await redis.scan(match=f"*_{quizz_id}_{company_id}")
    else:
        keys = await redis.scan(match=f"*_{company_id}")
    records = await redis.mget(keys[1])

    if records:
        return [json.loads(record, object_hook=datetime_parser) for record in records]

