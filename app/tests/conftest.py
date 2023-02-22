import asyncio
import pytest
import pytest_asyncio

from typing import AsyncGenerator
from starlette.testclient import TestClient
from httpx import AsyncClient

#import your app
from app import system_config
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_app():
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
