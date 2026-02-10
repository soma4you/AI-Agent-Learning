from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

from pathlib import Path
import json

path = Path('history.jsonl')
path.touch()
    
from dotenv import load_dotenv
load_dotenv()

system_prompt = '''
# Role: Solver Expert
# Task: Provide optimal solution in Korean.

# Output Format (Mandatory):
**1) 정의:** [Clear definition & summary]
**2) 이유(중요성):** [Why it matters & its value]
**3) 쉬운 예시:** [Analogy or practical example]

# Rules:
- Professional/friendly tone. 
- Explain simply complex terms.
- All output MUST be in Korean.
'''

# llm
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)

# prompt
prompt = ChatPromptTemplate.from_messages([
    ('system', system_prompt),
    MessagesPlaceholder(variable_name="history"),  # 대화 기록 삽입 위치
    ("user", "{question}")
])

# history
history = ChatMessageHistory()

# chain
chain = prompt | llm | StrOutputParser()

def show_messages():
    print('='*50)
    for i, msg in enumerate(history.messages[-2:]):
        role = '사용자' if msg.type == 'human' else 'AI'
        save_message(role, msg.content)
        print(f'{role}> {msg.content}\n')

def request(question:str):
    history.add_user_message(question)
    ai_msg = chain.invoke({'question': question, 'history': history.messages})
    history.add_ai_message(ai_msg)

# 챗 메시지 읽어오기
def load_message():
    with path.open('r', encoding='utf-8') as f:
        questions = []
        for line in f.readlines():
            data = json.loads(line)
            
            if str(data).startswith("사용자>"):
                questions.append(str(data).strip("사용자> "))
    return questions

# 챗 메시지 파일로 저장
def save_message(role, content):
    with path.open('a', encoding='utf-8') as f:
        data = json.dumps(f'{role}> {content}', ensure_ascii=False)
        f.write(data + '\n')
        

def main():
    questions = load_message()
    if len(questions) == 0:
        questions = ['REST API란?', '클라우드 컴퓨팅이 뭐야?', 'RAG 어떤 구조야?']
        
    print(f'대화를 시작합니다. 종료를 원하시면 "exit" 를 입력하세요!\n')
    while True:
        # request
        question = questions.pop() if len(questions) > 0 else input('질문: ').strip()
        
        if question == 'exit':
            print('프로그램이 종료되었습니다.')
            break
        else:
            request(question)
            show_messages()

if __name__ == '__main__':    
    main()
    
    