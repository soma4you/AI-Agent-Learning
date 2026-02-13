import streamlit as st
from typing import Annotated, TypedDict, List  # 데이터 타입 정의도구
from operator import add
from langgraph.graph import StateGraph, START, END
from PIL import Image, ImageDraw, ImageFont
import textwrap
from io import BytesIO
from pathlib import Path

class ChefState(TypedDict):
    messages: Annotated[List[str], add]

    # 방문 부서 체크 리스트
    execution_path: Annotated[List[str], add]
    
    scores: Annotated[List[int], add]
    errors: Annotated[List[str], add]


def planner_node(state: ChefState):
    """[기획부] 메뉴 계획을 세우고, 업무 기록(execution_path)를 남깁니다."""

    return {
        "messages": ["기획부: 오늘의 업무 계획을 세웠습니다."],
        "execution_path": ["기획부(planner)"],
        "scores": [30],
    }

def cook_node(state: ChefState):
    """[제작부] 요리를 완성하고, 업무을 기록합니다."""
    return {
        "messages": ["제작부: 주문하신 요리를 완성했습니다."],
        "execution_path": ["제작부(cook)"],
        "scores": [10],
        "errors": ["조리 실패: 재료 부족"]
    }

def review_node(state: ChefState):
    """[검수부] 품질 검사를 마치고, 업무 기록(execution_path)를 남깁니다."""

    return {
        "messages": ["검수부: 품질 검사를 완료했습니다. - 이상무."],
        "execution_path": ["검수부(reviewer)"],
        "scores": [40],
    }

# 1. 위기관리부 노드 수정 (에러 중복 추가 방지)
def error_handler_node(state: ChefState):
    """[위기관리부] 에러가 발생했을 때 처리하는 부서"""
    return {
        "messages": ["시스템 알림: 에러가 발생하여 작업을 중단합니다."],
        "execution_path": ["위기관리부(Error)"],
        "scores": [0],
    }

# 2. 도식화 함수 수정 (색상 오타 수정 및 에러 표시 로직 개선)
def draw_path_map(state):
    paths = state['execution_path']
    scores = state['scores']
    errors = state['errors']
    
    img = Image.new("RGB", size=(1000,250), color=(255,255,255))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(str(Path("c:/windows/fonts/batang.ttc")), 18)
    except:
        font = ImageFont.load_default()
    
    width, height = 210, 135
    start_x, start_y = 50, 50 
    
    for i, node_name in enumerate(paths):
        # 1. 부서 이름이 들어갈 네모 상자
        draw.rectangle([start_x, start_y, start_x+width, height], outline=(0,0,0), width=2)
       
        # 2. 상자 안에 부서 이름
        draw.text((start_x+20, 60), f"{i+1}. {node_name}", font=font, fill=(0,0,0))
        
        # 2-1. 상자 안에 점수
        draw.text((start_x+65, 85), f"점수: {scores[i]}", font=font, fill=(0,0,255))
        
        # 3. 다음 부서가 있다면 빨간색 선 그리기
        if i < len(paths) - 1:
            draw.line([start_x+200, 85, start_x+250, 85], fill=(255,0,0), width=3)
        
        # 4. 에러 메시지 표시 로직 수정
        # '제작부'에서 에러가 났을 때 해당 상자에만 에러가 표시되도록 조건 변경
        if errors and "cook" in node_name:
            draw.text((start_x+20, 110), f"에러: {errors[0][:10]}...", font=font, fill=(255,0,0))
        
        start_x += 250 

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
    
# 회사 오픈
workflow = StateGraph(ChefState)

# 작업 부서 등록
workflow.add_node("planner", planner_node)
workflow.add_node("cook", cook_node)
workflow.add_node("review", review_node)
workflow.add_node("error_handler", error_handler_node)

# 작업 흐름 설정
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "cook")
# workflow.add_edge("cook", "review")


# def role(state):
#     if state['errors']:
#         return "error_handler"
#     else:
#         return "review"
workflow.add_conditional_edges("cook", lambda state: "error_handler" if state["errors"] else "review")


workflow.add_edge("review", END)
workflow.add_edge("error_handler", END)

# 4. 설계도를 실제 실행 가능한 앱으로 만듭니다.
app = workflow.compile()


# --- [4단계] 실제로 시스템 가동하기 ---
st.title("에이전트 협업 시각화 테스트")
st.title("'멀티 에이전트' 로드맵")
if st.button("전 부서 협업 시스템 가동"):
    result = app.invoke({"messages":[]})

    print(result)
    
    st.divider()

    # 모든 부서가 기록한 내용을 화면에 뿌려줍니다.
    st.subheader("업무 기록 일지")
    for i, msg in enumerate(result["messages"]):
        st.info(msg)
    
    if result["errors"]:
        st.subheader('에러로그')
        for err in result["errors"]:
            st.error(err)
            
    st.subheader("최종 성과 점수")
    to= sum(result["scores"])
    st.success(f"결과: {to}")
    # for i, msg in enumerate(result["scores"]):
    #     st.info(msg)
    
    # 도식화
    load_map = draw_path_map(result)
    st.image(load_map)
    
    
    # 이미지 다운로드
    st.download_button(
        label="다운로드",
        data=load_map,
        file_name="downlaod.png",
        mime="image/png"
    )
