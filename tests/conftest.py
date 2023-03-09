import os
import asyncio

import pytest
import pytest_asyncio

from typing import AsyncGenerator
from starlette.testclient import TestClient
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from httpx import AsyncClient


#import your app
from app.main import app
#import your metadata
from app.db.models import metadata
#import your test urls for db
from app.utils.system_config import envs
#import your get_db func
from app.db.database import get_db, database


engine_test = create_async_engine(envs["DATABASE_URL_TEST"], poolclass=NullPool)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    await database.connect()
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    await database.disconnect()
    async with engine_test.begin() as conn:
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

