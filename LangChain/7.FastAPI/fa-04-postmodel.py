from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name:str
    price:float
    is_offer: bool

app = FastAPI(debug=True)
@app.get("/items")
async def create_item(item: Item):
    
    return {"message": f"/items/name={item.name}&price={item.price}"}

# 직렬화: 메모리에 저장된 변수값을 파일로 저장하는 것


    
    
    


