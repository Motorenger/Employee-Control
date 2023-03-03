from httpx import AsyncClient


async def test_get_users(ac: AsyncClient):
    response = await ac.get("/users/")
    assert response.status_code == 200
    assert response.json()["items"] == []


async def test_bad_create_user_not_passord(ac: AsyncClient):
    payload = {
      "password": "",
      "email": "test@test.test",
      "name": "test"
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_low_password(ac: AsyncClient):
    payload = {
      "password": "tet",
      "email": "test@test.test",
      "name": "test"
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_no_valid_email(ac: AsyncClient):
    payload = {
      "password": "test",
      "email": "test",
      "username": "test"
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 422


async def test_create_user_one(ac: AsyncClient, prepare_database):
    payload = {
      "password": "testtest",
      "email": "test1@test.com",
      "username": "test1",
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 1


async def test_create_user_error(ac: AsyncClient):
    payload = {
      "password": "testtest",
      "email": "test1@test.com",
      "username": "test2",
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 400


async def test_create_user_two(ac: AsyncClient):
    payload = {
      "password": "testtest",
      "email": "test2@test.com",
      "username": "test2",
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_create_user_three(ac: AsyncClient):
    payload = {
      "password": "testtest",
      "email": "test3@test.com",
      "username": "test3",
    }
    response = await ac.post("/users/create", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 3


async def test_get_users_list(ac: AsyncClient):
    response = await ac.get("/users/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3


async def test_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == 'test1@test.com'
    assert response.json()["username"] == 'test1'


async def test_bad_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/users/4")
    assert response.status_code == 404


async def test_update_user_one(ac: AsyncClient):
    payload = {
      "username": "test1NEW"
    }
    response = await ac.put("/users/1", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 1


async def test_get_user_by_id_updates(ac: AsyncClient):
    response = await ac.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["username"] == 'test1NEW'


async def test_update_user_not_exist(ac: AsyncClient):
    payload = {
      "username": "test1NEW",
    }
    response = await ac.put("/users/4", json=payload)
    assert response.status_code == 404


async def test_delete_user_one(ac: AsyncClient):
    response = await ac.delete("/users/1")
    assert response.status_code == 204


async def test_get_users_list_after_delete(ac: AsyncClient):
    response = await ac.get("/users/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2


async def test_bad_login_try(ac: AsyncClient):
    payload = {
        "email": "test2@test.com",
        "password": "tess",
    }
    response = await ac.post("/auth/login/", json=payload)
    assert response.status_code == 422


tokens = {
    "user_two": ""
}


async def test_login_try(ac: AsyncClient):
    payload = {
        "email": "test2@test.com",
        "password": "testtest",
    }
    response = await ac.post("/auth/login/", json=payload)
    tokens["user_two"] = response.json()['access_token']
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'


async def test_auth_me(ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {tokens.get('user_two')}",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()['username'] == "test2"
    assert response.json()['email'] == "test2@test.com"
    assert response.json()['id'] == 2


async def test_bad_auth_me(ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer test",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 401
