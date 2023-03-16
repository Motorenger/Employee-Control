from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params, paginate

from databases import Database


from db.database import get_db
from schemas.user_schemas import User, UserCreate, UserUpdate
from schemas.invite_schemas import InvitesList
from schemas.request_schemas import RequestList
from services.user_logic import UserService, UserActionsService
from utils.auth import get_user


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=Page[User])
async def users_list(params: Params = Depends(), current_user: User = Depends(get_user), db: Database = Depends(get_db)) -> Page:
    user_service = UserService(db=db)

    users = await user_service.get_users()
    return paginate(users.users, params)


@router.post("/create", response_model=User)
async def users_create(user: UserCreate, db: Database = Depends(get_db)) -> User:
    user_service = UserService(db=db)

    user = await user_service.create_user(user=user)
    return user


@router.get("/{user_id}", response_model=User)
async def users_retrieve(user_id: int = None, current_user: User = Depends(get_user), db: Database = Depends(get_db)) -> User:
    user_service = UserService(db=db)

    user = await user_service.retrieve_user(user_id=user_id)
    return user


@router.put("/{user_id}", response_model=User)
async def users_update(user_id: int, user_data: UserUpdate, current_user: User = Depends(get_user), db: Database = Depends(get_db)) -> User:
    user_service = UserService(db=db, current_user=current_user)

    user = await user_service.update_user(user_id=user_id, user_data=user_data)
    return user


@router.delete("/{user_id}", status_code=204)
async def users_delete(user_id: int, current_user: User = Depends(get_user), db: Database = Depends(get_db)):
    user_service = UserService(db=db, current_user=current_user)

    await user_service.delete_user(user_id=user_id)


# Actions

@router.get("/me/invites", response_model=InvitesList)
async def invites_list(current_user: User = Depends(get_user),
                       db: Database = Depends(get_db)) -> InvitesList:
    user_service = UserActionsService(db=db, current_user=current_user)

    invites = await user_service.get_invites()
    return invites


@router.post("/me/invites/accept/{invite_id}", status_code=201)
async def invite_accept(invite_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                        ):
    user_service = UserActionsService(db=db, current_user=current_user)

    await user_service.accept_invite(invite_id=invite_id)


@router.delete("/me/invites/decline/{invite_id}", status_code=204)
async def invite_decline(invite_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                        ):
    user_service = UserActionsService(db=db, current_user=current_user)

    await user_service.decline_invite(invite_id=invite_id)


@router.get("/me/requests", response_model=RequestList)
async def requests_list(current_user: User = Depends(get_user),
                       db: Database = Depends(get_db)) -> RequestList:
    user_service = UserActionsService(db=db, current_user=current_user)

    requests = await user_service.get_requests()
    return requests


@router.delete("/me/requests/decline/{request_id}", status_code=204)
async def request_decline(request_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                        ):
    user_service = UserActionsService(db=db, current_user=current_user)

    await user_service.decline_request(request_id=request_id)


@router.delete("/me/{company_id}/leave", status_code=204)
async def leave_company(company_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                        ):
    user_service = UserActionsService(db=db, current_user=current_user)

    await user_service.leave_company(company_id=company_id)
