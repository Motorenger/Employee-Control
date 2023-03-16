from httpx import AsyncClient


async def test_create_admin_not_auth(ac: AsyncClient):
    payload = {
        "user_id": 1
    }
    response = await ac.post('/company/2/admin/', json=payload)
    assert response.status_code == 403


async def test_create_admin_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "user_id": 100,
    }
    response = await ac.post('/company/2/admin/', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "it's not your company"


async def test_create_admin_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 100,
    }
    response = await ac.post('/company/2/admin/', headers=headers, json=payload)
    assert response.status_code == 404, response.json()
    assert response.json().get('detail') == "user with id 100 not found"


async def test_create_admin_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 2,
    }
    response = await ac.post('/company/100/admin/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "company with id 100 not found"


async def test_create_admin_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 1,
    }
    response = await ac.post('/company/2/admin/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


async def test_create_admin_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 3,
    }
    response = await ac.post('/company/2/admin/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


# admin-list
async def test_admin_list_not_auth(ac: AsyncClient):
    response = await ac.get('/company/2/admins')
    assert response.status_code == 403


async def test_admin_list_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/100/admins', headers=headers)
    assert response.status_code == 404


async def test_admin_list_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/2/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('admin')) == 2


# admin-remove
async def test_admin_remove_not_auth(ac: AsyncClient):
    response = await ac.delete('/company/2/admin/1')
    assert response.status_code == 403


async def test_admin_remove_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/2/admin/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'user with id 100 not found'


async def test_admin_remove_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/100/admin/1', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'company with id 100 not found'


async def test_admin_remove_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/2/admin/1', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "it's not your company"


async def test_admin_remove_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }

    response = await ac.delete('/company/2/admin/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_admin_list_success_after_remove(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/2/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('admin')) == 1


async def test_admin_list_control(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/company/1/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('admin')) == 0