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
from app.db.database import Base
#import your test urls for db
from app.utils.system_config import envs
#import your get_db func
from app.db.database import get_db
from app.db.models import User

test_db: Database = Database(envs["TEST_DATABASE_URL"], force_rollback=True)


def override_get_db() -> Database:
    return test_db


engine_test = create_async_engine(envs["TEST_DATABASE_URL"], poolclass=NullPool)


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
    await test_db.connect()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_db.disconnect()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = override_get_db
    print(app.dependency_overrides)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac