from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# (.env) 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

# Chat 모델 객체 생성
model = ChatOpenAI(model='gpt-4o-mini')

# 프롬프트 객체 생성 => HumanMessage(content="내 이름은 홍길동이야")
prompt = ChatPromptTemplate.from_template('{input}')

# 체인 구성 (| : 파이프라인)
# 입력(dict) -> ChatPromptTemplate -> ChatOpenAI -> StrOutputParser -> 문자열 결과
chain = prompt | model | StrOutputParser() # 익명객체(=이름이 없는 객체)

user_input = "내 이름은 '홍길동'이야."
print(f"질문1: {user_input} /응답 >>> {chain.invoke({'input':user_input})}")
'''결과 :
안녕하세요,  홍길동님! 어떻게 도와드릴까요?
'''