import streamlit as st
from typing import Annotated, TypedDict, List  # 데이터 타입 정의도구
from operator import add
from langgraph.graph import StateGraph, START, END
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path

class ChefState(TypedDict):
    messages: Annotated[List[str], add]

    # 방문 부서 체크 리스트
    execution_path: Annotated[List[str], add]


def plannig_department(state: ChefState):
    """[기획부] 메뉴 계획을 세우고, 업무 기록(execution_path)를 남깁니다."""

    return {
        "messages": ["기획부: 오늘의 업무 계획을 세웠습니다."],
        "execution_path": ["기획부(planner)"]
    }

def cooking_department(state: ChefState):
    """[제작부] 요리를 완성하고, 업무을 기록합니다."""
    return {
        "messages": ["제작부: 주문하신 요리를 완성했습니다."],
        "execution_path": ["제작부(cook)"],
    }

def reviewer_department(state: ChefState):
    """[검수부] 품질 검사를 마치고, 업무 기록(execution_path)를 남깁니다."""

    return {
        "messages": ["검수부: 품질 검사를 완료했습니다. - 이상무."],
        "execution_path": ["검수부(reviewer)"],
    }

def draw_path_map(paths):
    """에이전트들이 이동한 경로를 리스트로 받아 화살표로 그림을 그립니다."""
    
    # paths = state['execution_path']
    img = Image.new("RGB", size=(800,150), color=(2555,255,255))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(str(Path("c:/windows/fonts/batang.ttc")), 18)
    except:
        font = ImageFont.load_default()
    
    
    # 사각형 가로*세로
    width, height = 200, 100
    
    # 시작 좌표
    start_x, start_y = 50, 50 # 첫 번째 상자를 그릴 시작 위치(가로 좌표)
    for i, node_name in enumerate(paths):
        # 1. 부서 이름이 들어갈 네모 상자를 그립니다.
        draw.rectangle([start_x, start_y, start_x+width, height], outline=(0,0,0), width=2)
        # 2. 상자 안에 부서 이름을 씁니다.
        draw.text((start_x+20, 65), f"{i+1}. {node_name}", font=font, fill=(0,0,0))
        
        # 3. 다음 부서가 있다면 빨간색 화살표(선)를 그립니다.
        if i < len(paths) - 1:
            draw.line([start_x+200, 75, start_x+250, 75], fill=(255,0,0), width=3)
        
        start_x += 250 # 다음 상자를 위해 가로 위치를 옆으로 옮깁니다.

    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
    
# 회사 오픈
workflow = StateGraph(ChefState)

# 작업 부서 등록
workflow.add_node("planner", plannig_department)
workflow.add_node("cook", cooking_department)
workflow.add_node("reviewer", reviewer_department)

# 작업 흐름 설정
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "cook")
workflow.add_edge("cook", "reviewer")
workflow.add_edge("reviewer", END)

# 4. 설계도를 실제 실행 가능한 앱으로 만듭니다.
app = workflow.compile()


# --- [4단계] 실제로 시스템 가동하기 ---
st.title("에이전트 협업 시각화 테스트")
st.title("'멀티 에이전트' 로드맵")
if st.button("전 부서 협업 시스템 가동"):
    # 초기 게시판 내용을 비워서 업무를 시작합니다.
    initial_state = {"messages":[]}

    # 지도를 따라 부서별로 일이 진행됩니다.
    result = app.invoke(initial_state)

    st.divider()
    st.subheader("실시간 협업 로드맵")

    # 모든 부서가 기록한 내용을 화면에 뿌려줍니다.
    # for i, msg in enumerate(final_outcome["messages"]):
    #     st.write(f"[{i+1}번째 부서] {msg}")
    
    st.write(result['execution_path'])
    load_map = draw_path_map(result['execution_path'])
    st.image(load_map)
    
    st.download_button(
        label="다운로드",
        data=load_map,
        file_name="downlaod.png",
        mime="image/png"
    )
