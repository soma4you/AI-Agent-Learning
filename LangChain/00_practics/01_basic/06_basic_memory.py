from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

model = init_chat_model(
    model='gpt-4o-mini', 
    temperature = 0.7,  # 창의성(0.0 ~ 1.0)
    timeout = 10,       # 응답 대기 시간(초) - 무한 대기 방지
    max_tokens = 1000,  # 용량(응답 최대 길이 제한)
    max_retries = 1     # 안전성(자동 재시도 횟수)
)



# --------------------------------------------------
# 단일 메시지 입력 - 객체 형태
# --------------------------------------------------
system_message = SystemMessage(content='당신은 20년 경력의 수학 교사 입니다.')
human_message = HumanMessage(content='안녕하세요. 궁금한게 있어요!')
messages = [system_message, human_message]
result = model.invoke(messages)
print(result.content)



# --------------------------------------------------
# 다중 메시지 입력(메모리 구현) - 객체 형태
# --------------------------------------------------
messages = [
    SystemMessage(content='당신은 20년 경력의 수학 전문 선생님입니다.'),
    HumanMessage(content='저는 24살 홍길동입니다.'),
    AIMessage(content='반갑습니다, 홍길동님! 무엇을 도와드릴까요?'),
    HumanMessage(content='저의 이름과 나이가 뭐였죠?')
]
print(model.invoke(messages).content)



# --------------------------------------------------
# 다중 메시지 입력(메모리 구현) - 딕셔너리 형태
# --------------------------------------------------
messages = [
    {'role':'system', 'content':'당신은 20년 경력의 수학 전문 선생님입니다.'},
    {'role':'user', 'content':'저는 24살 홍길동입니다.'},
    {'role':'assistant', 'content':'반갑습니다, 홍길동님! 무엇을 도와드릴까요?'},
    {'role':'user', 'content':'저의 이름과 나이가 뭐였죠?'},
]
print(model.invoke(messages).content)
