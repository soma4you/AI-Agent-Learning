import streamlit as st

from typing import Annotated, TypedDict  # 데이터 타입 정의도구

import operator  # 내역 누적

from langgraph.graph import StateGraph, END


# --- [1단계] 공용 게시판(State) 만들기 ---
# 모든 부서가 같이 보고 내용을 적는 공유 문서
class ChefState(TypedDict):
    messages: Annotated[list[str], operator.add]


# --- [2단계] 각 부서(Node)의 업무 정의하기 ---
def plannig_department(state: ChefState):
    """[기획부서] 사용자의 요청을 보고 무엇을 할지 계획을 세웁니다."""

    st.write(
        "🔍 **[기획부]** : 손님이 다양한 케이크를 원하세요. 레시피 개발이 필요해요."
    )
    return {"messages": ["기획부: 고구마 케이크 레시피 찾기 계획 수립"]}


def cooking_department(state: ChefState):
    """[제작부서] 기획서가 넘어오면 실제로 요리(실행)를 합니다."""
    st.write("🛠️ **[제작부]** : 기획서 확인 완료! 지금 바로 케이크를 만듭니다.")
    # 게시판에 제작 완료 메시지를 추가합니다.
    return {"messages": ["제작부: 달콤한 고구마 케이크 완성!"]}


# --- [3단계] 부서 배치 및 결재 라인(Graph) 연결 ---
# 1. 우리 식당의 업무 지도(Graph)를 그리기 시작합니다.
workflow = StateGraph(ChefState)

# 2. 식당에 부서들을 배치합니다 (Node 추가)
workflow.add_node("planner", plannig_department)
workflow.add_node("cook", cooking_department)

# 3. 부서 간의 이동 경로를 설정합니다 (Edge 연결)
workflow.set_entry_point("planner")
workflow.add_edge("planner", "cook")
workflow.add_edge("cook", END)

# 4. 설계도를 실제 실행 가능한 앱으로 만듭니다.
app = workflow.compile()


# --- [4단계] 실제로 시스템 가동하기 ---
st.title("분업 시스템")

if st.button("협업 시스템 가동"):
    # 초기 게시판 내용을 비워서 업무를 시작합니다.
    initial_state = {"messages": []}

    # 지도를 따라 부서별로 일이 진행됩니다.
    final_outcome = app.invoke(initial_state)

    st.divider()
    st.subheader("공용 게시판 최종 기록")

    # 모든 부서가 기록한 내용을 화면에 뿌려줍니다.
    for msg in final_outcome["messages"]:
        st.write(msg)
