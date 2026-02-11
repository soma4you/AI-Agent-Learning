from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

@tool
def multiply(a: int, b: int):
    """두 정수의 곱을 반환합니다.
        Args:
            a (int): 첫 번째 숫자
            b (int): 두 번째 숫자
        Returns:
            int: 두 수의 곱
    """
    return a * b

print(f"도구 이름:{multiply.name}")
print(f"도구 설명:{multiply.description}")

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
tools = [multiply]
prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 수학 계산을 도와주는 만능 계산기입니다.'),
    ('user', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad')
])

agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

exec = AgentExecutor(
    agent=agent, # 에이전트
    tools=tools, # 도구
    verbose=True, # 디버깅
    handle_parsing_errors=True # 오류 처리 옵션
)

result = exec.invoke({'input':'100 * 10 = ?'})
print(result['output'])