from httpx import AsyncClient


async def test_bad_create_user_not_passord(ac: AsyncClient, users_tokens):
    payload = {
      "password": "",
      "email": "test@test.test",
      "name": "test"
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_low_password(ac: AsyncClient, users_tokens):
    payload = {
      "password": "tet",
      "email": "test@test.test",
      "name": "test"
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_no_valid_email(ac: AsyncClient, users_tokens):
    payload = {
      "password": "test",
      "email": "test",
      "username": "test"
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 422


async def test_create_user_one(ac: AsyncClient, users_tokens):
    payload = {
      "password": "testtest",
      "email": "test1@test.com",
      "username": "test1",
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 1


async def test_create_user_error(ac: AsyncClient, users_tokens):
    payload = {
      "password": "testtest",
      "email": "test1@test.com",
      "username": "test2",
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 400


async def test_create_user_two(ac: AsyncClient, users_tokens):
    payload = {
      "password": "testtest",
      "email": "test2@test.com",
      "username": "test2",
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_create_user_three(ac: AsyncClient, users_tokens):
    payload = {
      "password": "testtest",
      "email": "test3@test.com",
      "username": "test3",
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 3

"""
Auth
"""

async def test_bad_login_try(ac: AsyncClient, users_tokens):
    payload = {
        "email": "test2@test.com",
        "password": "tess",
    }
    response = await ac.post("/auth/login", json=payload)
    assert response.status_code == 422


async def test_login_try(ac: AsyncClient, users_tokens):
    payload = {
        "email": "test2@test.com",
        "password": "testtest",
    }
    response = await ac.post("/auth/login", json=payload)
    users_tokens["user_two"] = response.json().get('token')
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'


async def test_auth_me(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()['username'] == "test2"
    assert response.json()['email'] == "test2@test.com"
    assert response.json()['id'] == 2


async def test_bad_auth_me(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer test",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 401


"""
Task 7
"""


async def test_get_users_list(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3


async def test_get_users_list_unauth(ac: AsyncClient, users_tokens):
    response = await ac.get("/users/")
    assert response.status_code == 403


async def test_get_user_by_id(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.get("/users/1", headers=headers)
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['email'] == "test1@test.com"
    assert response.json()['username'] == "test1"

async def test_get_user_by_id_unauth(ac: AsyncClient, users_tokens):
    response = await ac.get("/users/1")
    assert response.status_code == 403


async def test_bad_get_user_by_id(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.get("/users/4", headers=headers)
    assert response.status_code == 404


async def test_update_user_one_bad(ac: AsyncClient, users_tokens):
    payload = {
      "username": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.put("/users/1", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_update_user_one_good(ac: AsyncClient, users_tokens):
    payload = {
      "username": "test2NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.put("/users/2", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()['id'] == 2


async def test_get_user_by_id_updates(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.get("/users/2", headers=headers)
    assert response.status_code == 200
    assert response.json()['id'] == 2
    assert response.json()['email'] == "test2@test.com"
    assert response.json()['username'] == "test2NEW"

async def test_delete_user_one_bad(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.delete("/users/1", headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_delete_user_one_good(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_two')}",
    }
    response = await ac.delete("/users/2", headers=headers)
    assert response.status_code == 204


async def test_login_user_one_(ac: AsyncClient, users_tokens):
    payload = {
        "email": "test1@test.com",
        "password": "testtest"
    }
    response = await ac.post("/auth/login", json=payload)
    users_tokens["user_one"] = response.json().get('token')
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'


async def test_get_users_list_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('user_one')}",
    }
    response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2

async def test_g():
    assert True == True