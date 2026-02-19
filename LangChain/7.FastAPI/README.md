# FastAPI Basics

FastAPI의 기본 개념과 주요 기능을 학습하는 실습 코드입니다.

## 📂 파일 목록

### 1. `fa-01-basic-server.py` (Basic Server)

- **목표**: FastAPI 서버 구동 및 기본 라우팅 이해
- **핵심**: `FastAPI()` 인스턴스 생성, `@app.get("/")` 데코레이터 사용

### 2. `fa-02-pathparameter.py` (Path Parameters)

- **목표**: URL 경로에 변수를 포함하여 데이터를 전달받는 방법 학습
- **핵심**: `/items/{item_id}`와 같이 중괄호를 사용하여 경로 매개변수 선언

### 3. `fa-03-datavalidation.py` (Query Parameters & Validation)

- **목표**: 쿼리 매개변수 사용 및 데이터 유효성 검사
- **핵심**: `Query` 클래스를 사용하여 길이 제한(`min_length`, `max_length`) 및 필수 여부 설정

### 4. `fa-04-postmodel.py` (Request Body with Pydantic)

- **목표**: POST 요청으로 데이터를 전달받고 Pydantic 모델로 구조화
- **핵심**: `BaseModel`을 상속받아 데이터 스키마 정의(`Item`), 요청 본문(Body) 처리

### 5. `fa-05-responsemodel.py` (Response Model)

- **목표**: 응답 데이터의 구조를 정의하고 필터링
- **핵심**: `response_model` 매개변수를 사용하여 응답 스키마 지정, 민감한 정보 제외 등

### 6. `fa-06-difference.py` (TypedDict vs Pydantic)

- **목표**: Python `TypedDict`와 Pydantic `BaseModel`의 차이점 이해
- **핵심**: `TypedDict`는 딕셔너리 타입 힌팅, `Pydantic`은 데이터 검증 및 파싱 기능 제공

### 7. `fa-07-error.py` (Error Handling)

- **목표**: HTTP 예외 처리 방법 학습
- **핵심**: `HTTPException`을 사용하여 에러 상태 코드 및 메시지 반환
