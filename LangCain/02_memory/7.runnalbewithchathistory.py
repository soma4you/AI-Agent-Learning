from callfunction import *

# 세션별 대화 기록 저장
# 대화 기록을 메모리(컴퓨터의 임시 저장 공간)에 저장하는 클래스
from langchain_core.chat_history import InMemoryChatMessageHistory
# 세션별 대화 기록을 관리하는 래퍼
# 이 인터페이스는 "메시지 기록을 사용하는 모든 객체가 따라야 할 규칙"입니다.
from langchain_core.runnables.history import RunnableWithMessageHistory

# 사용자 메시지를 표현하는 객체
from langchain_core.messages import HumanMessage

model = ChatOpenAI(model='gpt-4o-mini')

# 세션 저장소 생성
store = {}

def get_session_history(session_id:str):
    if session_id not in store:
        # 생성
        store[session_id] = InMemoryChatMessageHistory()
    
    # print(store[session_id])
    return store[session_id]

with_msg_history = RunnableWithMessageHistory(
    model,
    get_session_history
)

requests = [
    {'session_id': 'abc2', 'message': '안녕?, 만난서 반가워. 나느  24살 홍길동이라고 해'},
    {'session_id': 'abc2', 'message': '내 이름 뭐라고?'},
    {'session_id': 'abc1', 'message': '내 이름 뭐라고?'},
    {'session_id': 'abc2', 'message': '아까 내가 무슨 얘기했어?'},
]


for req in requests:
    config = {'configurable': {'session_id': req['session_id']}}
    
    response = with_msg_history.invoke(
        [HumanMessage(content=req['message'])],
        config=config
    )
    print('-'*50)
    print(f'Human({req["session_id"]}): {req["message"]}')
    print (f'AI: {response.content}\n')
    

print('스트리밍 방식 구현 ', '-'*50)
config = {'configurable': {'session_id': 'abc2'}}
for chunk in with_msg_history.stream(
    [HumanMessage(content='내가 어느 나라 사람인지 맞춰보고, 그 나라의 문화에 대해서 말해보세요.')],
    config=config):
    
    print(chunk.content, end='', flush=True)