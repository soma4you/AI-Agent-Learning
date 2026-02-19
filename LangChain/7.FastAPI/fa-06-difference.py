from pydantic import BaseModel
from typing import TypedDict, Optional


class UserModel(BaseModel):
    username: str
    age: int = 25
    
class UserTypedDict(TypedDict):
    username: str
    age: int


user1 = UserModel(username='hong')
print(user1)


user2 = UserModel(username='hong', age=20)
print(user2)


user2 = UserTypedDict(username="Kim")
print(user2)

user3 = UserTypedDict= {"username":"홍길동", "age": 30}
print(user3)

if "test" not in user3:
    user3["test"] = False
    
print(user3)