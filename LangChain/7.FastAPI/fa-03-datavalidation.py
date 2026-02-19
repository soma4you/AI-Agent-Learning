from fastapi import FastAPI,Query

app = FastAPI(debug=True)

@app.get("")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/items/")
async def read_items(q: str = Query(None, min_length=3, max_length=50, title="검색어"),
                    limit: int = Query(10, gt=0, le=100) # gt: >, le: <=
                    ):
    return {"q": q, "limit": limit}