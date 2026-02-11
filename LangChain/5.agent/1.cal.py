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