from httpx import AsyncClient


async def test_pass_quizz_not_auth(ac: AsyncClient):
    response = await ac.post("quizzes/2/2/pass")
    assert response.status_code == 403


async def test_pass_quizz_not_found(ac: AsyncClient, users_tokens, quizz_pass_payload):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.post("quizzes/2/200/pass", headers=headers, json=quizz_pass_payload)

    assert response.status_code == 404
    assert response.json().get("detail") == "Quizz not found"


async def test_pass_quizz_wrong_payload(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    quizz_pass_payload = {
        "Hello_world:)": True
    }
    response = await ac.post("quizzes/2/2/pass", headers=headers, json=quizz_pass_payload)

    assert response.status_code == 422

async def test_pass_quizz_success_incorrect(ac: AsyncClient, users_tokens, quizz_pass_payload):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.post("quizzes/2/2/pass", headers=headers, json=quizz_pass_payload)

    assert response.status_code == 200
    assert response.json().get("record_average_result") == 0.0

async def test_pass_quizz_success_correct(ac: AsyncClient, users_tokens, quizz_pass_payload_correct):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.post("quizzes/2/2/pass", headers=headers, json=quizz_pass_payload_correct)

    assert response.status_code == 200
    assert response.json().get("record_average_result") == 10
