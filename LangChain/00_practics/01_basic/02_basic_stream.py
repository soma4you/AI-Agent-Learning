from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
load_dotenv()

model = init_chat_model(
    model='gpt-4o-mini', 
    temperature = 0.7,  # 창의성(0.0 ~ 1.0)
    timeout = 10,       # 응답 대기 시간(초) - 무한 대기 방지
    max_tokens = 1000,  # 용량(응답 최대 길이 제한)
    max_retries = 1     # 안전성(자동 재시도 횟수)
)

# ----------------------------------
# stream() : chunk(말뭉치) 단위로 잘라서 하나씩 답변 생성 -> UX 증가
# ----------------------------------
for chunk in model.stream("안녕하세요. 저는 홍길동입니다."):
    # print(chunk.text(), end='', flush=True)
    print(chunk.content, end='', flush=True) # chunk.text() : 결과값 같음
    
    # -- 출력 결과 --
    # 안녕하세요, 홍길동님! 어떻게 도와드릴 수 있을까요?
    
