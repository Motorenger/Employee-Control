from httpx import AsyncClient


async def test_create_quizz_not_auth(ac: AsyncClient):
    response = await ac.post("quizzes/2")
    assert response.status_code == 403


async def test_create_quizz_not_owner_or_admin(ac: AsyncClient, users_tokens, quizz_payload):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.post("quizzes/2", headers=headers, json=quizz_payload)
    assert response.status_code == 403


async def test_create_quizz_one_success(ac: AsyncClient, users_tokens, quizz_payload):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post("quizzes/2", headers=headers, json=quizz_payload)

    assert response.status_code == 201
    assert response.json().get("id") == 1
    assert response.json().get("title") == "Hello?"
    assert response.json().get("pass_freq") == 10


async def test_create_quizz_two_success(ac: AsyncClient, users_tokens, quizz_payload):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post("quizzes/2", headers=headers, json=quizz_payload)

    assert response.status_code == 201
    assert response.json().get("id") == 2
    assert response.json().get("title") == "Hello?"
    assert response.json().get("pass_freq") == 10

# Deleting quizz


async def test_delete_quizz_not_auth(ac: AsyncClient):
    response = await ac.delete("quizzes/2/1")
    assert response.status_code == 403


async def test_delete_quizz_not_owner_admin(ac: AsyncClient,  users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("quizzes/2/1", headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "You is not allowed"


async def test_delete_quizz_success(ac: AsyncClient,  users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("quizzes/2/1", headers=headers)
    assert response.status_code == 204
