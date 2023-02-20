import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(ac: AsyncClient):
    data = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == data
