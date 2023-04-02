import asyncio

import pytest

from typing import AsyncGenerator
from starlette.testclient import TestClient
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#import your app
from app.main import app
#import your metadata
from app.db.models import metadata
#import your test urls for db
from app.utils.system_config import envs
#import your get_db func
from app.main import get_db


engine = create_async_engine(envs["DATABASE_URL"], poolclass=NullPool)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_app():
    await get_db().connect()
    with TestClient(app) as client:   # context manager will invoke startup event 
        yield client


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    await get_db().connect()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    await get_db().disconnect()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session')
async def login_user(ac: AsyncClient, users_tokens: dict):
    async def __send_request(user_email: str, user_password: str):
        payload = {
            "email": user_email,
            "password": user_password,
        }
        response = await ac.post("/auth/login", json=payload)
        if response.status_code != 200:
            return response
        user_token = response.json().get('token')
        users_tokens[user_email] = user_token
        return response

    return __send_request


@pytest.fixture(scope='session')
def users_tokens():
    tokens_store = dict()
    return tokens_store


@pytest.fixture(scope='session')
def quizz_payload():
    return {
    "title": "Hello?",
    "pass_freq": 10,
    "questions": [
        {
            "title": "What is radius?",
            "correct_answer": 2,
            "answers": {
                "1": {
                    "answer": "Half of the circle lengh"
                },
                "2": {
                    "answer": "Answer 2"
                }
            }
        },
        {
            "title": "Where is piramid?",
            "correct_answer": 1,
            "answers": {
                "1": {
                    "answer": "Cosinus"
                },
                "2": {
                    "answer": "Sinus"
                }
            }
        }
    ]
}

@pytest.fixture(scope="session")
def quizz_pass_payload():
    payload = {
        "questions": {
            "1": {
                "answer": 1
            },
            "2": {
                "answer": 2
            }
        }
    }
   
    return payload

@pytest.fixture(scope="session")
def quizz_pass_payload_correct():
    payload = {
        "questions": {
            "1": {
                "answer": 2
            },
            "2": {
                "answer": 1
            }
        }
    }
   
    return payload
