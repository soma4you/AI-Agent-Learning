from fastapi import FastAPI

app = FastAPI(debug=True)

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

# uvicorn 파일명:객체명 -- reload
#.get(): 데이터 조회
#.post(): 데이터 생성
#.put(): 데이터 수정
#.delete(): 데이터 삭제