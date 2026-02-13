import streamlit as st
from typing import Annotated, TypedDict, List
from operator import add
from langgraph.graph import StateGraph, START, END


class ChefState(TypedDict):
    messages: Annotated[List[str], add]
    # 에러 발생
    errors: Annotated[List[dict], add]
    error_state: str


def planner_node(state: ChefState):
    """[기획부] 계획을 세우고, 업무 기록(execution_path)를 남깁니다."""
    step = state.get("step", 0) + 1
    return {
        "messages": ["info", "기획부: 오늘의 업무 계획을 세웠습니다."],
    }


def cook_node(state: ChefState):
    """[제작부] 요리를 완성하고, 업무을 기록합니다."""

    if "error_state" in state and state["error_state"] == "done":
        return {
            "messages": ["info", "제작부: 주문하신 요리를 완성했습니다."],
        }
    else:
        return {
            "messages": ["warning", "제작부: 재료 부족으로 요리가 지연되고 있습니다."],
            "errors": [
                {
                    "node": "제작부",
                    "why": "재료 부족",
                    "request": "밀가루가 부족합니다.",
                }
            ],
            "error_state": "waiting",
        }


def marketing_node(state: ChefState):
    """[홍보부] 메뉴를 홍보하고, 업무를 기록합니다."""
    return {
        "messages": ["info", "홍보부: 오늘의 메뉴를 SNS에 홍보했습니다."],
    }


def review_node(state: ChefState):
    """[검수부] 검수를 마치고, 업무 기록(execution_path)를 남깁니다."""
    return {
        "messages": ["info", "검수부: 품질 검사를 완료했습니다. - 이상무."],
    }


def delivery_node(state: ChefState):
    """[배달부] 배달을 마치고, 업무 기록(execution_path)를 남깁니다."""
    return {
        "messages": ["success", "배달부: 배달을 완료했습니다."],
    }


def error_check(state: ChefState):
    if state["error_state"] == "waiting":
        return "error"
    else:
        return "success"


def error_handler_node(state: ChefState):
    """[위기관리부] 에러가 발생했을 때 처리하는 부서"""
    msg = [e for e in state["errors"] if e is not None]

    for v in state["errors"]:
        msg = f"긴급상황! {v['node']} / {v['why']}: {v['request']}"

    error_msg = ["error", f"위기관리부: {msg}"]
    resolve_msg = ["success", "위기관리부: 부족한 밀가루를 공급합니다."]

    return {
        "messages": error_msg + resolve_msg,
        "error_state": "done",
    }


# 회사 오픈
workflow = StateGraph(ChefState)

# 작업 부서 등록
workflow.add_node("planner", planner_node)
workflow.add_node("cook", cook_node)
workflow.add_node("review", review_node)
workflow.add_node("error_handler", error_handler_node)
workflow.add_node("marketing", marketing_node)
workflow.add_node("delivery", delivery_node)

# 작업 흐름 설정
workflow.add_edge(START, "planner")

# 병렬 분기
workflow.add_edge("planner", "cook")
workflow.add_edge("planner", "marketing")
workflow.add_edge("marketing", END)

workflow.add_edge("error_handler", "cook")

# 조건 분기
workflow.add_conditional_edges(
    "cook",
    error_check,
    {
        "error": "error_handler",
        "success": "review",
    },
)

# 종료
workflow.add_edge("review", "delivery")
workflow.add_edge("review", END)

app = workflow.compile()

# UI
st.title("에이전트 협업 시각화 테스트")
if st.button("전 부서 협업 시스템 가동"):
    result = app.invoke({})

    print(result)

    st.divider()

    # 모든 부서가 기록한 내용을 화면에 뿌려줍니다.
    st.subheader("업무 기록 일지")
    for i, msg in enumerate(result["messages"]):
        if msg == "error":
            st.error(result["messages"][1 + i])
        elif msg == "success":
            st.success(result["messages"][1 + i])
        elif msg == "warning":
            st.warning(result["messages"][1 + i])
        elif msg == "info":
            st.info(result["messages"][1 + i])

    if "errors" in result:
        st.subheader("위기 관리부: 에러 감지")
        if len(result["errors"]) > 0:

            for err in result["errors"]:
                st.error(err)

    st.subheader("부서별 협업 플로우")

    # 도식화
    load_map = app.get_graph().draw_mermaid_png()
    st.image(load_map)

    # 이미지 다운로드
    st.download_button(
        label="다운로드", data=load_map, file_name="downlaod.png", mime="image/png"
    )
#--------------------------------------------------------------------------------------
# import streamlit as st
# from typing import Annotated, TypedDict, List
# from operator import add
# from langgraph.graph import StateGraph, START, END

# # 1. 상태 타입 정의를 개선 (메시지를 명확한 딕셔너리 형태로 변경)
# class ChefState(TypedDict):
#     messages: Annotated[List[dict], add]  # {"type": "info", "text": "..."} 형태
    
#     # 노드 경로
#     execution_path: Annotated[List[dict], add]
#     step: Annotated[int, lambda old, new: new]
#     last_id: Annotated[int, lambda old, new: new]
    
#     # 에러 발생
#     errors: Annotated[List[dict], add]
#     error_state: str

# def planner_node(state: ChefState):
#     """[기획부] 계획을 세우고, 업무 기록(execution_path)을 남깁니다."""
#     step = state.get("step", 0) + 1
#     return {
#         "messages": [{"type": "info", "text": "기획부: 오늘의 업무 계획을 세웠습니다."}],
#         "execution_path": [{"id": step, "node": "planner", "from": state.get('last_id')}],
#         "step": step,
#         "last_id": step
#     }

# def cook_node(state: ChefState):
#     """[제작부] 요리를 완성하거나 에러를 기록합니다."""
#     step = state.get("step", 0) + 1
     
#     if state.get("error_state") == "done":
#         return {
#             "messages": [{"type": "info", "text": "제작부: 주문하신 요리를 완성했습니다."}],
#             "execution_path": [{"id": step, "node": "cook", "from": state.get("last_id")}],
#             "step": step,
#             "last_id": step
#         }
#     else:
#         return {
#             "messages": [{"type": "warning", "text": "제작부: 재료 부족으로 요리가 지연되고 있습니다."}],
#             "execution_path": [{"id": step, "node": "cook", "from": state.get("last_id")}],
#             "errors": [{"node": "제작부", "why": "재료 부족", "request": "밀가루가 부족합니다."}],
#             "error_state": "waiting",
#             "step": step,
#             "last_id": step
#         }

# def marketing_node(state: ChefState):
#     """[홍보부] 메뉴를 홍보하고, 업무를 기록합니다."""
#     step = state.get("step", 0) + 1
#     return {
#         "messages": [{"type": "info", "text": "홍보부: 오늘의 메뉴를 SNS에 홍보했습니다."}],
#         "execution_path": [{"id": step, "node": "marketing", "from": state.get("last_id")}],
#         "step": step,
#         "last_id": step
#     }
    
# def review_node(state: ChefState):
#     """[검수부] 검수를 마치고, 업무 기록(execution_path)을 남깁니다."""
#     step = state.get("step", 0) + 1
#     return {
#         "messages": [{"type": "info", "text": "검수부: 품질 검사를 완료했습니다. - 이상무."}],
#         "execution_path": [{"id": step, "node": "review", "from": state.get("last_id")}],
#         "step": step,
#         "last_id": step
#     }

# def delivery_node(state: ChefState):
#     """[배달부] 배달을 마치고, 업무 기록을 남깁니다."""
#     step = state.get("step", 0) + 1
#     return {
#         "messages": [{"type": "success", "text": "배달부: 배달을 완료했습니다."}],
#         "execution_path": [{"id": step, "node": "delivery", "from": state.get("last_id")}], # 버그 수정: review -> delivery
#         "step": step,
#         "last_id": step
#     }

# def error_check(state: ChefState):
#     if state.get("error_state") == "waiting":
#         return "error"
#     return "success"
    
# def error_handler_node(state: ChefState):
#     """[위기관리부] 에러가 발생했을 때 처리하는 부서"""
#     step = state.get("step", 0) + 1
    
#     # 마지막 에러를 가져오는 안전한 로직
#     last_error = state.get("errors", [{}])[-1]
#     msg_text = f"긴급상황! {last_error.get('node', '알수없음')} / {last_error.get('why', '알수없음')}: {last_error.get('request', '원인불명')}"
    
#     msgs = [
#         {"type": "error", "text": f"위기관리부: {msg_text}"},
#         {"type": "success", "text": "위기관리부: 부족한 밀가루를 공급합니다."}
#     ]
    
#     return {
#         "messages": msgs,
#         "execution_path": [{"id": step, "node": "error_handler", "from": state.get("last_id")}],
#         "error_state" : "done",
#         "step": step,
#         "last_id": step
#     }

# # 워크플로우 생성
# workflow = StateGraph(ChefState)

# # 노드 추가
# workflow.add_node("planner", planner_node)
# workflow.add_node("cook", cook_node)
# workflow.add_node("review", review_node)
# workflow.add_node("error_handler", error_handler_node)
# workflow.add_node("marketing", marketing_node)
# workflow.add_node("delivery", delivery_node)

# # 작업 흐름 설정 (Edge)
# workflow.add_edge(START, "planner")

# workflow.add_edge("planner", "cook")
# workflow.add_edge("planner", "marketing")
# workflow.add_edge("marketing", END)

# workflow.add_edge("error_handler","cook")

# # 조건 분기
# workflow.add_conditional_edges(
#     "cook",
#     error_check,
#     {
#         "error": "error_handler",
#         "success": "review",
#     }
# )

# # 종료 분기
# workflow.add_edge("review", "delivery")
# workflow.add_edge("delivery", END)  # 명시적인 종료 추가
# workflow.add_edge("review", END)    # 리뷰 완료 직후에도 병렬로 종료되길 원한다면 유지

# app = workflow.compile()

# # === Streamlit UI ===
# st.title("에이전트 협업 시각화 테스트")

# if st.button("전 부서 협업 시스템 가동"):
#     # 가동 중 스피너 추가로 UX 개선
#     with st.spinner("부서별 협업 중..."):
#         result = app.invoke({})
    
#     st.divider()

#     st.subheader("📝 업무 기록 일지")
    
#     # 리팩토링된 메시지 파싱
#     for msg in result.get("messages", []):
#         msg_type = msg.get("type", "info")
#         msg_text = msg.get("text", "")
        
#         if msg_type == "error":
#             st.error(msg_text)
#         elif msg_type == "success":
#             st.success(msg_text)
#         elif msg_type == "warning":
#             st.warning(msg_text)
#         else:
#             st.info(msg_text)
    
#     if result.get("errors"):
#         st.subheader("🚨 위기 관리부: 에러 감지 내역")
#         for err in result.get("errors", []):
#             # 딕셔너리 내용을 예쁘게 포매팅
#             st.error(f"[{err.get('node')}] {err.get('why')} - {err.get('request')}")
            
#     st.subheader("📊 부서별 협업 플로우")
    
#     try:
#         load_map = app.get_graph().draw_mermaid_png()
#         st.image(load_map)
        
#         st.download_button(
#             label="그래프 다운로드",
#             data=load_map,
#             file_name="workflow_graph.png", # 오타 수정
#             mime="image/png"
#         )
#     except Exception as e:
#         st.warning("그래프 시각화 라이브러리를 불러오는 데 실패했습니다.")