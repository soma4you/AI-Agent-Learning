from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """`a`와 `b` 덧셈.

    Args:
        a: First int
        b: Second int
    """
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """`a`와 `b` 뺄셈.

    Args:
        a: First int
        b: Second int
    """
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """`a`와 `b` 곱셈.

    Args:
        a: First int
        b: Second int
    """
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """`a`와 `b` 나눗셈.

    Args:
        a: First int
        b: Second int
    """
    return a / b

# 도구 리스트
tools = [add, subtract, multiply, divide]

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-4o-mini")
agent = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

result = agent.run("3과 5를 더하고, 그 결과에 10을 곱한 다음, 마지막으로 2로 나눠줘")
print(result)
