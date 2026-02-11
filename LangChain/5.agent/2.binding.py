from langchain_core.tools import tool

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

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm  = ChatOpenAI(model='gpt-4o-mini', temperature=0)
llm_with_tools = llm.bind_tools(tools=[multiply])

res = llm_with_tools.invoke("10 곱하기 3은?")
print(res)
print(res.tool_calls)
