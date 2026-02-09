from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(temperature=0.5)

prompt = ChatPromptTemplate.from_messages([
    ('system', '너는 육군 베테랑 전투교관'),
    ('user', '12살 초등학생 남자 아이에게 {topic}을 이해하기 쉽게 설명해줘'),
    ('ai', '좋아. 학생에게 쉽게 설명해볼게') # AI Message
])

chain = prompt | llm

result = chain.invoke({'topic':'무인도에서 살아남는 법'})

print(result)