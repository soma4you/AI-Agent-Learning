from langchain_core.tools import tool
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


import streamlit as st

from dotenv import load_dotenv
load_dotenv()

# 요리사가 사용할 수 있는 도구 설명서

# 재료 가격
@tool
def check_ingredient_price(items: str) -> int:
    """식재료의 시장 가격을 조회합니다.

    Args:
        items (str): 식재료 이름

    Returns:
        int: 요청한 식재료의 가격을 반환합니다. 재료가 없는 경우 -1 반환.
    """
    return 29900

# 레시피
@tool
def get_recipi(menu: str) -> str:
    """요청한 요리, 음식의 조리법(레시피)를 반환합니다.

    Args:
        menu (str): 요리, 음식 메뉴 이름

    Returns:
        str: 조리법을 반환합니다.
    """
    return f"{menu}의 조리법은 다음과 같습니다."


llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)
tools = [check_ingredient_price, get_recipi]

tool_with_bind = llm.bind_tools(tools=tools)

prompt = ChatPromptTemplate.from_messages([
    ('system', "당신은 20년 경력의 친절한 조리사입니다. 사용자가 요청한 요리 메뉴에 대한 기본 정보를 조사하고, 필요한 재료와 가격, 레시피까지 정확할게 피드백합니다."),
    ('user', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad'),
])

st.title('요리사의 판단')
order = st.text_input("요리사에게 질문해보세요.(고등어 가격이 얼마인가요? 혹은 김치찌개 끓이 만드는 법)")
if order:
    response = tool_with_bind.invoke(order)
    order = ""
    if response.tool_calls:
        st.success(f"{response.tool_calls[0]['name']} 도구를 사용")
    else:
        st.info(f'죄송합니다. 저는 잘 몰라요.')
    
    
    

