import os
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", temperature=0.7)
# result = model.invoke("오늘 한국 날씨 어뗴?")
# print(result.content)

# -- 출력 결과 --
# 죄송하지만, 실시간 날씨 정보를 제공할 수는 없습니다. 한국의 날씨를 확인하시려면 날씨 관련 웹사이트나 앱을 이용하시거나 뉴스 채널을 참고하시기 바랍니다. 도움이 필요하시면 다른 질문 해주세요!


# tool vs Tool
# 직접 함수를 짜서 도구로 쓸 거라면? 👉 @tool
# 이미 만들어진 남의 코드나 복잡한 객체의 메서드를 도구로 등록만 하고 싶다면? 👉 Tool
from langchain.tools import tool
from langchain.tools import Tool

import requests

# 예시: 날씨 정보를 반환하는 도구 정의
@tool
def get_weather(location: str) -> str:
    """주어진 위치의 날씨 정보를 반환합니다.
        Args:
            location: e.g. Seoul, London, New York 
    """  # 이 설명이 AI에게 전달됩니다.
    
    # 날씨 API 키 불러오기
    weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&lang=kr&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    # return f"{location}의 현재 날씨는 {data}입니다."
    return f"{location}의 현재 날씨는 {data['weather'][0]['description']}이며, 기온은 {data['main']['temp']}도입니다."

''' 
-- 예시(Seoul) 응답 데이터(json) --
{
  "coord": {
    "lon": 126.9778,
    "lat": 37.5683
  },
  "weather": [
    {
      "id": 701,
      "main": "Mist",
      "description": "박무",
      "icon": "50n"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 1.76,
    "feels_like": 0.19,
    "temp_min": 1.76,
    "temp_max": 1.78,
    "pressure": 1019,
    "humidity": 100,
    "sea_level": 1019,
    "grnd_level": 1009
  },
  "visibility": 3500,
  "wind": {
    "speed": 1.54,
    "deg": 340
  },
  "clouds": {
    "all": 100
  },
  "dt": 1770723601,
  "sys": {
    "type": 1,
    "id": 8105,
    "country": "KR",
    "sunrise": 1770676069,
    "sunset": 1770714296
  },
  "timezone": 32400,
  "id": 1835848,
  "name": "Seoul",
  "cod": 200
}
'''


# -----------------------------------------------------------------------
# 에이전트 생성: create_tool_calling_agent vs initialize_agent
# -----------------------------------------------------------------------

# 1) create_tool_calling_agent: 도구 호출 에이전트 전용
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([   
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(model, tools=[get_weather], prompt=prompt)

# 실행기(Executor) 생성 - 이 부분이 핵심입니다!
agent_executor = AgentExecutor(agent=agent, tools=[get_weather], verbose=True)

# 실행 (agent.invoke 대신 executor.invoke 사용)
result = agent_executor.invoke({'input': '서울의 날씨 알려줘'})
print(result["output"])


# -----------------------------------------------------------------------
# 2) initialize_agent: 다양한 유형의 에이전트 생성 가능
# - 도구 호출 에이전트: AgentType.OPENAI_FUNCTIONS
# - 체인 오브 생각 에이전트: AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION 등
# - 도구 외에도 다양한 설정 가능 (예: 로깅 등)
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools=[get_weather],              # 도구 리스트
    llm=model,                        # 사용할 언어 모델
    agent=AgentType.OPENAI_FUNCTIONS, # 에이전트 유형
    verbose=True                      # 로깅 설정
)
result = agent.run("도쿄의 날씨 알려줘")
print(result)

