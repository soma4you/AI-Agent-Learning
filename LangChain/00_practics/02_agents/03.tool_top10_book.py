from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from typing import List, Dict, Any
import requests

import os
from dotenv import load_dotenv
load_dotenv()




# 1. 모델 설정
model = init_chat_model("gpt-4o-mini", temperature=0)

# 2. 도구 정의 (데코레이터 방식 권장)
@tool
def fetch_aladin_bestseller_top10() -> List[Dict[str, Any]]:
    """알라딘 베스트셀러 목록을 조회하고 Top 10개를 반환합니다."""
    url = "http://www.aladin.co.kr/ttb/api/ItemList.aspx"
    
    params = {
        "ttbkey": os.getenv("ALADIN_API_KEY"),
        "QueryType": "Bestseller",
        "MaxResults": 10,
        "start": 1,
        "SearchTarget": "Book",
        "output": "js",
        "Version": "20131101"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("item", [])[:10]

tools = [fetch_aladin_bestseller_top10]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

result = agent.run("알라딘 베스트셀러 Top 10 책 목록을 알려줘")
print(result)




# 공식 프롬프트에는 {tools}, {tool_names}, {agent_scratchpad}가 모두 포함됨
from langchain import hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# create_structured_chat_agent
# 여러 개의 입력 변수(Argument)를 가진 도구를 에이전트가 정확하게 사용할 수 있도록 설계된 에이전트 생성 함수
# 이 에이전트는 JSON 형식으로 복잡한 인자값을 주고받는데 특화
from langchain.agents import create_structured_chat_agent, AgentExecutor

agent = create_structured_chat_agent(model, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent, # 에이전트
    tools=tools, # 도구 리스트
    verbose=True, # 출력 상세 모드
    handle_parsing_errors=True # 오류 처리 옵션
)
result = agent_executor.invoke({"input": "알라딘 베스트셀러 Top 10 책 목록을 알려줘"})
print(result["output"])
