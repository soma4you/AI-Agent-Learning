from callfunction import *

from langchain_core.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory

llm = ChatOpenAI(model='gpt-4o-mini')
memory = ConversationBufferWindowMemory(return_messages=True, k=2)
prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 사용자의 이전 대화를 기억하는 전문 비서입니다. 모든 응답은 글자수 300자 내외'),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{input}')
])

chain = prompt | llm

# 연속 대화 시뮬레이션(사용자 입력을 순차적으로 물어보도록 코딩)
inputs = ['안녕, 나는 홍길동이야.!',
          'AI에이전트 프로젝트 아이디어 추천 3개', 
          '너가 제일 강력 추천 아이디어를 기준으로 간단히 구체회해줘.',
          '필요한 기술 스택과 예상 개발 기간은 어떻게 되?',
          'MVP 방식을 원해. 최소한의 기능으로 반응을 확인하고 싶어.',
          '다시한번 검토해서 구현 및 서비스 가능한지 확인해줘. (yes or no)',
          '근데 내 이름 기억해?'
]


for i in inputs:
    # 메모리에 저장된 값을 꺼내라
    history = memory.load_memory_variables({})['history']
    result = chain.invoke({'input': i, 'history':history})
    print(f'''==================================\n사용자: {i}\nAI: {result.content}''')
    memory.save_context({'input': i}, {'output':result.content})