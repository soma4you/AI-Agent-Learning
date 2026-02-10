from callfunction import ChatOpenAI, ChatPromptTemplate, StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

model = ChatOpenAI(model='gpt-4o-mini')
mgs_placeholder = MessagesPlaceholder('chat_history',optional=True)
prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 사용자의 이전 대화를 기억하고 있는 전문 비서입니다.'),
    (mgs_placeholder),
    ('user', '{input}'),
])
chain = prompt | model | StrOutputParser()

# 대화 기록
chat_history = [] # UserMessage, AIMessage

print('대화를 시작합니다. 종료를 원하시면 "exit" 를 입력하세요.' )

while True:
    user_input = input('사용자: ')
    if user_input.lower().strip() == 'exit':
        break
    
    response = chain.invoke({
        'input': user_input,
        'chat_history': chat_history
    })
    print(f'AI: {response}\n')
    print(mgs_placeholder.format_messages())
    
    # 역할별로 질문과 응답을 구분해서 대화 기록
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response))
    