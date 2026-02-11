# LangChain Agent 기초

LangChain의 Agent 기능을 활용하여 도구(Tool)를 정의하고, LLM이 스스로 계획(Plan)하고 실행(Execute)하는 과정을 학습한 코드입니다.

## 📂 파일 설명

### 1. 기본 도구 활용

- **1.cal.py**: 기본적인 계산기 도구 등을 정의하고 에이전트가 이를 활용하는 가장 기초적인 예제입니다.
- **2.binding.py**: LLM에 도구를 바인딩(Binding)하여 함수 호출(Function Calling)이 가능하도록 설정하는 방법을 다룹니다.

### 2. 에이전트 사고 과정

- **3.thought.py**: 에이전트가 문제를 해결하기 위해 스스로 생각하고 추론하는 과정(Chain of Thought)을 시각화거나 제어하는 예제입니다.

### 3. 요리사 에이전트 (Cook Agent) 실습

- **4.cook_plan.py**: 요리 레시피나 계획을 수립하는 에이전트 구현 파일입니다.
- **5.cook_tool.py**:
  - 커스텀 도구(`@tool`) 정의: `check_ingredient`, `check_ingredient_price`, `get_recipi`
  - `create_openai_functions_agent`를 사용한 에이전트 생성
  - 사용자의 요청("김치찌개 먹을래")에 대해 재료 확인, 가격 계산, 레시피 안내를 순차적으로 수행하는 종합 예제입니다.

## 🚀 실행 방법

```bash
# 가상환경 활성화 후
python 5.cook_tool.py
```
