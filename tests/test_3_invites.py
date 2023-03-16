from httpx import AsyncClient


# send invite tests

async def test_send_invite_not_auth(ac: AsyncClient):
    payload = {
        "to_user_id": 1,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_send_invite_not_found_user(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_user_id": 100,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This user not found'


async def test_send_invite_not_found_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 100,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'This company not found'


async def test_send_invite_not_your_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "it's not your company"


async def test_send_invite_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_user_id": 2,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_send_invite_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_user_id": 1,
        "from_company_id": 2,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_send_invite_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "to_user_id": 3,
        "from_company_id": 1,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_send_invite_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "to_user_id": 3,
        "from_company_id": 2,
        "invite_message": "string"
    }
    response = await ac.post("/invite/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# My invites

async def test_my_invites_not_auth(ac: AsyncClient):
    response = await ac.get("/invite/my")
    assert response.status_code == 403


async def test_my_invites_user_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result')) == 1


async def test_my_invites_user_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result')) == 1


async def test_my_invites_user_three(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/invite/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result')) == 2


# Company invites

async def test_company_invites_not_auth(ac: AsyncClient):
    response = await ac.get("/invite/company/1/")
    assert response.status_code == 403


async def test_invites_company_one_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/company/1/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "it's not your company"


async def test_invites_company_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/company/1/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result')) == 2


async def test_invites_company_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/company/2/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result')) == 2


# cancel-invite

async def test_cancel_invite_not_auth(ac: AsyncClient):
    response = await ac.delete("/invite/1/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_cancel_invite_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/invite/100/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Invite not found"


async def test_cancel_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete("/invite/1/", headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "it's not your company"


async def test_cancel_invite_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/invite/1/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# Accept invite

async def test_accept_invite_not_auth(ac: AsyncClient):
    response = await ac.get("/invite/1/accept/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_accept_invite_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/100/accept/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Invite not found"


async def test_accept_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/2/accept/", headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "It is not your invite"


async def test_accept_invite_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/2/accept/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# decline-invite

async def test_decli_invite_not_auth(ac: AsyncClient):
    response = await ac.get("/invite/1/decline/")
    assert response.status_code == 403
    assert response.json().get('detail') == "Not authenticated"


async def test_decli_invite_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/invite/100/decline/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Invite not found"


async def test_decli_invite_not_your(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/invite/3/decline/", headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "User does not have an invite to the company"


async def test_decli_invite_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/invite/3/decline/", headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


async def test_members_only_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 2


async def test_accept_requests(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/invite/4/accept/", headers=headers)
    assert response.status_code == 200


async def test_members_after_accept(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/company/2/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('users')) == 3