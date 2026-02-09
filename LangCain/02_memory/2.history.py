from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

'''
과거 대화 문자열 + 현재 질문
→ 하나의 프롬프트로 합침
→ 모델에게 전달
→ 모델이 ‘맥락을 이해한 척’ 답하는지 확인
'''
model = ChatOpenAI(model='gpt-4o-mini')

chat_history = 'user: 내 이름은 홍길동이야.' \
               'ai: 반가워요 홍길동님!'

prompt = ChatPromptTemplate.from_template('이전대화: {chat_history}\n질문: {input}')


chain = prompt | model | StrOutputParser()

user_input = "내 이름은 뭐야?"

result = chain.invoke({'chat_history':chat_history, 'input':user_input})

print(f"응답: {result}")
'''결과:
당신의 이름은 홍길동입니다.
'''