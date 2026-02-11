from langchain_core.tools import tool
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv
load_dotenv()

# 요리사가 사용할 수 있는 도구 설명서

# 필요 재료 
@tool
def check_ingredient(menu: str) -> str:
    """요청한 요리에 필요한 식재료를 반환합니다.

    Args:
        menu (str): 요리, 음식 메뉴 이름

    Returns:
        str: 요청한 요리의 식재료
    """
    
    return "김치, 두부, 대파, 마늘, 국간장, 돼지고기(선택)"

# 재료 가격
@tool
def check_ingredient_price(items: str) -> int:
    """식재료의 시장 가격을 조회합니다.

    Args:
        items (str): 식재료 이름

    Returns:
        int: 요청한 식재료의 가격을 반환합니다. 재료가 없는 경우 -1 반환.
    """
    menu = {'김치': 9000, '두부': 1000, '대파': 2300, '마늘': 500, '국간장': 2500, '돼지고기': 14500}
    if items in menu:
        return menu[items]
    
    return -1

# 레시피
@tool
def get_recipi(menu: str) -> str | None:
    """요청한 요리, 음식의 조리법(레시피)를 반환합니다.

    Args:
        menu (str): 요리, 음식 메뉴 이름

    Returns:
        str: 조리법을 반환합니다. 조리법이 없는 경우 None.
    """
    if menu == "김치찌개":
        return f"{menu}의 조리법은 다음과 같습니다. 재료 준비-고기볶기-김치추가-양념 넣고, 완성! 맛있게 드세요."
    
    return None


llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)
tools = [check_ingredient, check_ingredient_price, get_recipi]

prompt = ChatPromptTemplate.from_messages([
    ('system', "당신은 20년 경력의 친절한 조리사입니다. \
        사용자가 요청한 요리 메뉴에 대한 기본 정보를 조사하고, \
        필요한 재료와 가격, 레시피까지 정확하게 피드백합니다. \
        만약 도구에 없는 메뉴인 경우 '죄송합니다. 등록된 레시피가 없습니다'라고 말하세요."),
    ('user', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad'),
])

agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

exec = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

res = exec.invoke({'input':'오늘 저녁은 김치찌개를 먹을거야'})
print(res['output'])

print("-"*50)

res = exec.invoke({'input':'해물 파스타 조리법 알려줘'})
print(res['output'])