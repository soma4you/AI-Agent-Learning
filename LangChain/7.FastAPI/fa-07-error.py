from fastapi import FastAPI, HTTPException

app = FastAPI()
@app.get("/error")
def raise_error():
    # 404: 요청한 데이터가 없는 경우
    # 500: 문법 에러
    raise HTTPException(status_code=404, detail="Item not found.")