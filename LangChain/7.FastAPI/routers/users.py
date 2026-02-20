from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from database import get_db_connect

# prefix = 공통 경로, tags = 프로젝트 문서 분류 기준
router = APIRouter(prefix="/users", tags= ["Users"])
# router = APIRouter(prefix="/items", tags= ["Items"])
# router = APIRouter(prefix="/paymests", tags= ["Payments"])

class UserBase(BaseModel):
    name:str = Field(description="사용자 이름")
    email:str = Field(description="사용자 이메일", examples=["sample@test.com"])
    
class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass
    
class UserResponse(UserCreate):
    id:int|None


class User(UserBase):
    id:int

# create(insert)
@router.post("/", response_model=UserResponse)
async def user_create(user: UserCreate):
    conn = get_db_connect()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO users(name, email) VALUES (?, ?)",
                (user.name, user.email)
    )
    conn.commit()
    conn.close()
    return UserResponse(id=cur.lastrowid, **user.model_dump())

# read All
@router.get("/", response_model=List[User])
async def list_users():
    conn = get_db_connect()
    
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    for user in users:
        
        print(f"type:{type(user)}")
    return [dict(user) for user in users]

# read one
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    conn = get_db_connect()
    cur = conn.cursor()
    
    user = cur.execute("SELECT * FROM users WHERE id = (?)", (user_id, )).fetchone()
    conn.close()
    
    if user is None:
        raise HTTPException(404, detail="user not found")
    return dict(user)

# update
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id:int, user: UserUpdate):
    conn = get_db_connect()
    cur = conn.cursor()
    
    cur.execute("UPDATE users SET name = ?, email = ? WHERE id= ?",
                (user.name, user.email, user_id)
    )
    conn.commit()
    conn.close()
    return UserResponse(id=user_id, **user.model_dump())

# delete
@router.delete("/{user_id}")
async def delete_user(user_id: int):
    with get_db_connect() as conn:
        cur = conn.execute("DELETE FROM users WHERE id= ?", (user_id, ))
        if cur.rowcount == 0:
            raise HTTPException(404, "User not found")
        
    return {"message": f"User {user_id} deleted successfully"}