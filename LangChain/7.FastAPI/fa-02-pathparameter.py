from fastapi import FastAPI

app = FastAPI(debug=True)

@app.get("")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    
    return {"message": f"/items/{item_id}"}

@app.get("/items")
async def show_items(skip: int, limit: int):
    
    return {"message": f"/items/skip={skip}&limit={limit}"}


    
    
    


