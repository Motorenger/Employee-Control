from httpx import AsyncClient


async def test_create_admin_not_auth(ac: AsyncClient):
    response = await ac.post("companies/2/members/admin/1")
    assert response.status_code == 403


async def test_create_admin_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.post('/companies/2/members/admin/100', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It is not your company"


async def test_create_admin_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post('/companies/200/members/admin/2', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_create_admin_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post('/companies/2/members/admin/1', headers=headers)
    assert response.status_code == 201


async def test_create_admin_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }

    response = await ac.post('/companies/2/members/admin/3', headers=headers)
    assert response.status_code == 201


# admin-list
async def test_admin_list_not_auth(ac: AsyncClient):
    response = await ac.get('/companies/2/members/admins')
    assert response.status_code == 403


async def test_admin_list_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/companies/200/members/admins', headers=headers)
    assert response.status_code == 404


async def test_admin_list_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/companies/2/members/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 2


# admin-remove
async def test_admin_remove_not_auth(ac: AsyncClient):
    response = await ac.delete('/companies/2/members/admins1')
    assert response.status_code == 403


async def test_admin_remove_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/companies/2/members/admins/1', headers=headers)
    assert response.status_code == 404


async def test_admin_remove_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/companies/2/members/admin/1', headers=headers)
    assert response.status_code == 204





async def test_admin_list_success_after_remove(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/companies/2/members/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 1


async def test_admin_list_control(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/companies/1/members/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 0