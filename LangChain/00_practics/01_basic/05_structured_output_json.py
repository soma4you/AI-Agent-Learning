'''
구조화된 답변 생성 (Structured Outputs)
--> 답변을 특정 형태로 **파싱**할 때 사용

- 스키마 생성
    1. pydantic : 파싱 + 데이터 검증 및 직렬화 지원
    2. json 스키마 : 파싱 (영어/숫자/언더스코어/대시만 사용 가능)
- model.with_structured_output()
'''

from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
load_dotenv()

json_schema = {
    "title": "Movie",
    "description": "A movie with details",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "The title of the movie"
        },
        "year": {
            "type": "integer",
            "description": "The year the movie was released"
        },
        "director": {
            "type": "string",
            "description": "The director of the movie"
        },
        "rating": {
            "type": "number",
            "description": "The movie's rating out of 10"
        }
    },
    "required": ["title", "year", "director", "rating"]
}

model = init_chat_model(
    model='gpt-4o-mini', 
    temperature = 0.7,  # 창의성(0.0 ~ 1.0)
    timeout = 10,       # 응답 대기 시간(초) - 무한 대기 방지
    max_tokens = 1000,  # 용량(응답 최대 길이 제한)
    max_retries = 1     # 안전성(자동 재시도 횟수)
)
    
model_with_json_schema = model.with_structured_output(schema=json_schema)
result = model_with_json_schema.invoke('영화 기생충에 대해 설멸해 주세요')

print(result)
# -- 출력 결과 --
# {'title': 'Parasite', 'year': 2019, 'director': 'Bong Joon-ho', 'rating': 8.6}

print(f"제목: {result['title']}")
print(f"개봉일: {result['year']}")
print(f"감독: {result['director']}")
print(f"평점: {result['rating']}")

# -- 출력 결과 --
'''
제목: 기생충
개봉일: 2019
감독: 봉준호
평점: 8.6
'''