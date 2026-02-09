from callfunction import *
# 추가

from langchain_community.chat_message_histories import ChatMessageHistory # 대화 기록 관리해주는 클래스
from langchain_openai import OpenAI, ChatOpenAI

# 1.LLM 초기화

llm = OpenAI(temperature=0.5)
history = ChatMessageHistory()

def show_history():
    '''현재까지 대화 기록을 보기 좋게 출력'''
    print('\nshow_history() >>> ')
    # print(histtory)
    # print(histtory.messages)
    for i, msg in enumerate(history.messages):
        role = '사용자' if msg.type == 'human' else 'AI'
        print(f'{role}> {msg.content}\n')
    print('='*50)
    
def main():
    print(f'''대화를 시작합니다.(종료: 'exit')''')
    while True:
        user_input = input('사용자>>> ')
        if user_input.lower().strip() == 'exit':
            print('프로그램을 종료합니다.')
            break
        
        # 사용자 메시지 기록
        history.add_user_message(user_input)
        
        # 응답 요청
        ai_response = llm.invoke(user_input)
        
        # ai 메시지 기록
        history.add_ai_message(ai_response)
        
        # 응답 출력
        # print(f'AI: {ai_response}')
        
        # 대화 기록 출력
        show_history()

if __name__ == "__main__":
    main()