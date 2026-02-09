# PromptTemplate, ChatPromptTemplate 차이점
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import OpenAI
import dotenv
dotenv.load_dotenv()

llm = OpenAI(temperature=0.5)

# 단순 문자열 기반 프롬프트 입력시 사용
prompt = PromptTemplate(
    input_variables=['topic'],
    template='다음 주제에 대해 간단히 설명해줘:{topic}'
)
chain = prompt | llm
print(f"PromptTemplate >>>\n{chain.invoke({'topic': '선형대수'})}\n")

# 대화 기반 프롬프트 입력시 사용
prompt = ChatPromptTemplate.from_messages([
    ('system', '너는 친절한 코칭 리더야.'),  # System Message
    ('user', '다음 주제에 대해 5살 어린이도 알기 쉽게 간단히 설명해줘:{topic}') # User Message
])
chain = prompt | llm
print(f"ChatPromptTemplate >>>\n{chain.invoke({'topic': '선형대수'})}")