from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params, paginate

from databases import Database


from db.database import get_db
from schemas.user_schemas import User, UserCreate, UserUpdate
from services.logic import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=Page[User])
async def users_list(params: Params = Depends(), db: Database = Depends(get_db)) -> Page:
    user_service = UserService(db=db)

    users = await user_service.get_users()
    return paginate(users.users, params)


@router.post("/create", response_model=User)
async def users_create(user: UserCreate, db: Database = Depends(get_db)) -> User:
    user_service = UserService(db=db)

    user = await user_service.create_user(user=user)
    return user


@router.get("/{user_id}", response_model=User)
async def users_retrieve(user_id: int = None, db: Database = Depends(get_db)) -> User:
    user_service = UserService(db=db)

    user = await user_service.retrieve_user(user_id=user_id)
    return user


@router.put("/{user_id}", response_model=User)
async def users_update(user_id: int, user_data: UserUpdate, db: Database = Depends(get_db)) -> User:
    user_service = UserService(db=db)

    user = await user_service.update_user(user_id=user_id, user_data=user_data)
    return user


@router.delete("/{user_id}", status_code=204)
async def users_delete(user_id: int, db: Database = Depends(get_db)):
    user_service = UserService(db=db)

    await user_service.delete_user(user_id=user_id)
