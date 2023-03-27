from httpx import AsyncClient


# send invite tests

async def test_send_invite_not_auth(ac: AsyncClient):
    payload = {
        "user_id": 1,
        "message": "string"
    }
    response = await ac.post("companies/1/invite", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_send_invite_not_found_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('test1@test.com')}",
    }
    payload = {
        "user_id": 100,
        "message": "string"
    }
    response = await ac.post("companies/1/invite", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This user not found'


async def test_send_invite_not_found_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('test1@test.com')}",
    }
    payload = {
        "user_id": 1,
        "message": "string"
    }
    response = await ac.post("companies/100/invite", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This company not found'


async def test_send_invite_not_your_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens.get('test2@test.com')}",
    }
    payload = {
        "user_id": 1,
        "message": "string"
    }
    response = await ac.post("companies/1/invite", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It is not your company"


async def test_send_invite_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "user_id": 2,
        "message": "string"
    }
    response = await ac.post("companies/1/invite", json=payload, headers=headers)
    assert response.status_code == 201


async def test_send_invite_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 1,
        "message": "string"
    }
    response = await ac.post("companies/2/invite", json=payload, headers=headers)
    assert response.status_code == 201


async def test_send_invite_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "user_id": 3,
        "message": "string"
    }
    response = await ac.post("companies/1/invite", json=payload, headers=headers)
    assert response.status_code == 201


async def test_send_invite_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "user_id": 3,
        "message": "string"
    }
    response = await ac.post("companies/2/invite", json=payload, headers=headers)
    assert response.status_code == 201


# My invites

async def test_my_invites_not_auth(ac: AsyncClient):
    response = await ac.get("users/me/invites")
    assert response.status_code == 403


async def test_my_invites_user_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("users/me/invites", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('invites')) == 1


async def test_my_invites_user_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("users/me/invites", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('invites')) == 1


async def test_my_invites_user_three(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("users/me/invites", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('invites')) == 2


# Company invites

async def test_company_invites_not_auth(ac: AsyncClient):
    response = await ac.get("companies/1/invites")
    assert response.status_code == 403


async def test_invites_company_one_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("companies/1/invites", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It is not your company"


async def test_invites_company_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("companies/1/invites", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2


async def test_invites_company_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("companies/2/invites", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2


# cancel-invite

async def test_cancel_invite_not_auth(ac: AsyncClient):
    response = await ac.delete("companies/1/invite/1")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_cancel_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("companies/1/invite/1", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It is not your company"


async def test_cancel_invite_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("companies/1/invite/1", headers=headers)
    assert response.status_code == 204


# Accept invite

async def test_accept_invite_not_auth(ac: AsyncClient):
    response = await ac.post("users/me/invites/accept/1")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_accept_invite_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.post("users/me/invites/accept/100", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Invite not found"


async def test_accept_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.post("users/me/invites/accept/2", headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "It is not your invite"


async def test_accept_invite_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.post("users/me/invites/accept/2", headers=headers)
    assert response.status_code == 201


# decline-invite

async def test_decline_invite_not_auth(ac: AsyncClient):
    response = await ac.delete("users/me/invites/decline/1")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_decli_invite_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("users/me/invites/decline/1000", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Invite not found"


async def test_decli_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("users/me/invites/decline/3", headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User does not have an invite to the company"


async def test_decli_invite_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete("users/me/invites/decline/3", headers=headers)
    assert response.status_code == 204


async def test_members_only_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/companies/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 1


async def test_accept_requests(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.post("users/me/invites/accept/4", headers=headers)
    assert response.status_code == 201


async def test_members_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/companies/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('users')) == 2