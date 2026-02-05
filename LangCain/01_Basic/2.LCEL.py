# 모듈 불러오기
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# api_key 설정
import dotenv
dotenv.load_dotenv()

# 1. 모델 설정(필수)
model = ChatOpenAI(model='gpt-4o-mini')

# 2. 프롬프트 설정(필수)
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 실력이 20년 경력의 베테랑 번역가야. 입력되는 영어를 자연스러운 한국어로 번역해줘."),
    ("user",'{input}')
])

# parser = StrOutputParser() # 객체생성

# 3. 체인 생성 (LCEL의 핵심)
chain = prompt | model | StrOutputParser() # 익명객체(=이름이 없는 객체)

result = chain.invoke({'input':'Then took the other, as just as fair And having perhaps the better claim'})
print("result:\n\n", result)


