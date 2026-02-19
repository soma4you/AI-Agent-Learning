from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    """
    사용자 데이터 정의
    """
    name:str                    # 필수값
    email: Optional[str] = None # 선택값
    

app = FastAPI(debug=True)

@app.get("/users/{userName}", response_model=User)
async def get_user(userName: str):
    
    return User(name=userName)



    
    
    


