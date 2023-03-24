from httpx import AsyncClient

# send request

async def test_send_request_not_auth(ac: AsyncClient):
    payload = {
        "company_id": 0,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_send_request_not_found_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "company_id": 100,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This company not found'


async def test_send_request_from_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "company_id": 1,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User is already a member of the company"


async def test_send_request_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "company_id": 2,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User is already a member of the company"


async def test_send_request_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "company_id": 1,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload, headers=headers)
    assert response.status_code == 201


async def test_send_request_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "company_id": 1,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload, headers=headers)
    assert response.status_code == 201


async def test_send_request_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "company_id": 2,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload, headers=headers)
    assert response.status_code == 201


# my requests

async def test_my_requests_not_auth(ac: AsyncClient):
    response = await ac.get("users/me/requests")
    assert response.status_code == 403


async def test_my_requests_user_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("users/me/requests", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('requests')) == 0


async def test_my_requests_user_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("users/me/requests", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('requests')) == 1


async def test_my_requests_user_three(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("users/me/requests", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('requests')) == 1


# company requests

async def test_company_requests_not_auth(ac: AsyncClient):
    response = await ac.get("/companies/1/requests")
    assert response.status_code == 403


async def test_requests_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/companies/100/requests", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "This company not found"


async def test_requests_company_one_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/companies/1/requests", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It is not your company"


async def test_requests_company_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/companies/1/requests", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2


# request cancel


async def test_cancel_requests_not_auth(ac: AsyncClient):
    response = await ac.delete("users/me/requests/decline/1")
    assert response.status_code == 403


async def test_cancel_request_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("users/me/requests/decline/1", headers=headers)
    assert response.status_code == 204


# accept request

async def test_accept_requests_not_auth(ac: AsyncClient):
    response = await ac.post("companies/1/requests/accept/2")
    assert response.status_code == 403


async def test_accept_requests_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post("companies/1/requests/accept/2", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It is not your company"


# declin request


async def test_decline_request_not_auth(ac: AsyncClient):
    response = await ac.delete('companies/1/requests/3')
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_decline_request_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('companies/1/requests/2', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It is not your company"


async def test_decline_request_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('companies/1/requests/2', headers=headers)
    assert response.status_code == 204


#===============================


async def test_members_only_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/companies/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 2


async def test_accept_requests(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post("companies/2/requests/accept/3", headers=headers)
    assert response.status_code == 201


async def test_members_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/companies/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 3


# ===========

async def test_kick_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("/companies/2/members/3", headers=headers)
    assert response.status_code == 204


async def test_members_after_kick(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/companies/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 2


async def test_leave_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.delete("users/me/2/leave", headers=headers)
    assert response.status_code == 204


async def test_members_after_leave(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/companies/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 1


async def test_send_request_three_again_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "company_id": 2,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload, headers=headers)
    assert response.status_code == 201


async def test_accept_request_three(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post("companies/2/requests/accept/4", headers=headers)
    assert response.status_code == 201


async def test_send_request_four_again_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "company_id": 2,
        "message": "string"
    }
    response = await ac.post("companies/request", json=payload, headers=headers)
    assert response.status_code == 201


async def test_accept_request_four(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post("companies/2/requests/accept/5", headers=headers)
    assert response.status_code == 201