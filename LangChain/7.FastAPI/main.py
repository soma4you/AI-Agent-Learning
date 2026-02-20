from fastapi import FastAPI
from routers import users

app = FastAPI()

@app.get("/")
def root():
    return{"message":"200 OK"}

app.include_router(users.router)