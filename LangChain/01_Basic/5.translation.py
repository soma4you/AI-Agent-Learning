from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import dotenv
dotenv.load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')
prompt = ChatPromptTemplate.from_template(
    '다음 한국어 문장을 영어로 번역하되, 반드시 10단어 이내로 간결하게 답해줘.\n문장: {korean_text}'
)
chain = prompt | model | StrOutputParser() # 익명객체(=이름이 없는 객체)

user_input = "오늘 날씨가 너무 좋아서 근처 공원에 산책을 가고 싶다."
result = chain.invoke({'korean_text': user_input})

print(f"입력 >>> {user_input}")
print(f"결과 >>> {result}")