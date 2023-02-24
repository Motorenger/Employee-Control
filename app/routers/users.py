from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, Params, paginate

from databases import Database


from db.database import get_db
from schemas.user_schemas import User, UserCreate, UserUpdate
from utils.hashing import get_password_hash


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=Page[User])
async def users_list(params: Params = Depends(), db: Database = Depends(get_db)):
    await db.connect()
    query = "SELECT * FROM users"
    users = await db.fetch_all(query)
    return paginate(users, params)


@router.post("/create", response_model=User)
async def users_create(user: UserCreate, db: Database = Depends(get_db)):
    user = user.dict()
    user["password"] = get_password_hash(user["password"])
    user["is_active"] = False
    user["date_joined"] = datetime.now()

    query = """INSERT INTO users(email, username, password, is_active, date_joined)
               VALUES (:email, :username, :password, :is_active, :date_joined)
            """
    await db.execute(query=query, values=user)
    users = await db.fetch_all(query="SELECT * FROM users")
    return users[-1]


@router.get("/{user_id}", response_model=User)
async def users_retrieve(user_id: int, db: Database = Depends(get_db)):
    query = "SELECT * FROM users WHERE id = :id"
    user = await db.fetch_one(query, values={"id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
async def users_update(user_id: int, user_data: UserUpdate, db: Database = Depends(get_db)):
    query = """UPDATE users
               SET username = :username, email = :email
               WHERE id = :id;
            """
    values = user_data.dict()
    values["id"] = user_id
    await db.execute(query, values=values)
    query = "SELECT * FROM users WHERE id = :id"
    user = await db.fetch_one(query, values={"id": user_id})
    return user


@router.delete("/{user_id}",)
async def users_delete(user_id: int, db: Database = Depends(get_db)):
    query = "SELECT * FROM users WHERE id = :id"
    user = await db.fetch_one(query, values={"id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    query = "DELETE FROM users WHERE id = :id"
    await db.execute(query, values={"id": user_id})
    return "User deleted successfully"
