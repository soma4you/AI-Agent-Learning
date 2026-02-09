from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(temperature=0.5)

prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 친절한 여행 가이드야'),
    ('user', '나는 {city}에 여행 가고 싶어'),
    ('ai', '좋아요. {city}에 유명한 맛집을 3개 추천드려요.'), # AI Message
    ('user', '유명한 맛집 말고 현지 로컬 푸드가 좋아'),
    ('ai', '그렇군요. 제주도에는 현지 로컬들이 많이 찾는 맛집도 많아요. 어떤 음식을 좋아하시나요?'),
    ('user', '면요리 좋아해'),
])

chain = prompt | llm

result = chain.invoke({'city':'제주도'})

print(result)
