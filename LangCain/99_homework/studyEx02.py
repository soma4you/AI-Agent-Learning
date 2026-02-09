'''
# 목표: 
LangChain 라이브러리를 활용하여 '장기 기억'을 가진 AI '여행 비서 챗봇'을 구현

## 구현 조건:
- 챗봇 페르소나: AI 여행 비서 "트래블GPT"
- 주요 기능: 고객이 여러 도시를 순서대로 여행할 때, 이전 대화 내용을 기억하여 연결된 맞춤 일정, 숙소, 음식을 제안

- 사용 기술:
    - LLM 모델: ChatOpenAI(model="gpt-4o-mini") 사용
    - 메모리 구현: ConversationSummaryMemory를 사용하여 장기 대화 기억 구현

- 출력 조건: 답변에 반드시 "이전 여행 내용을 바탕으로 추천드리면..."이라는 문구를 포함

- 대화 시나리오:
    - 사용자: "부산 → 여수 → 강릉" 순서로 도시를 이동
    - 챗봇: 이전 도시에서 한 활동을 기억하고 다음 도시에서 "연결된 여행 루트"나 "테마별 추천" (가족/커플/힐링)을 제안
'''
import os
import sys
from typing import Dict, Tuple

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# ==========================================
# [설정 및 상수 정의]
# ==========================================

# 시스템 프롬프트 (여행 큐레이터 페르소나 및 제약조건)
SYSTEM_PROMPT_TEXT = '''
Role: 20yr Pro Travel Guide. Output: Korean.
Input Processing: 
- Typo/Ambiguity: Auto-correct to most likely city/country or ask for clarification.
- Country Input: Select representative [City]. 
Logic:
- 1st City: 1 sentence [Stay/Schedule/Menu] keywords.
- City N (N>1): 1 sentence total.
  * Start: "이전 여행 내용을 바탕으로 추천드리면, "
  * Link: Mention ONLY the *Immediate Previous* city (N-1) feedback/vibe.
  * Content: Current city's [Stay/Schedule/Menu] keywords.
Constraint: Strict single-sentence only. Maintain context of visited cities.
'''
#Constraint: Strict single-sentence. High-density keywords. Recall full trip history.

# 메뉴 옵션 정의
MENU_OPTIONS: Dict[str, Tuple[str, str]] = {
    '1': ('트래블GPT', '여행하고 싶은 곳을 알려주세요'),
    '2': ('종료', '프로그램이 종료되었습니다'),
}

# 사용자 입력 명령어 상수
CMD_BACK = '0'


# ==========================================
# [AI 로직 클래스]
# ==========================================
class TravelCurator:
    """
    LangChain을 이용해 여행 추천을 수행하는 봇 클래스
    """
    def __init__(self, model_name: str = 'gpt-4o-mini'):
        # LLM 모델 초기화
        self.llm = ChatOpenAI(model=model_name)
        
        # 대화 요약 메모리 초기화
        self.memory = ConversationSummaryMemory(
            llm=self.llm, 
            return_messages=True
        )
        
        # 프롬프트 템플릿 구성
        self.prompt_template = ChatPromptTemplate.from_messages([
            ('system', SYSTEM_PROMPT_TEXT),
            MessagesPlaceholder(variable_name="history"), # 대화 기록 주입 위치
            ('user', '{input}')
        ])
        
        # 실행 체인 구성 (Prompt -> LLM -> String Output)
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def get_response(self, user_input: str) -> str:
        """
        사용자 입력에 대한 AI 응답을 생성하고 메모리를 업데이트합니다.
        """
        # 1. 현재 대화 기록 로드
        history = self.memory.load_memory_variables({})['history']
        
        # 2. 체인 실행 (답변 생성)
        ai_response = self.chain.invoke({
            'input': user_input, 
            'history': history
        })
        
        # 3. 대화 맥락 저장 (User Input & AI Output)
        self.memory.save_context(
            inputs={'input': user_input}, 
            outputs={'output': ai_response}
        )
        
        return ai_response


# ==========================================
# [UI 및 실행 로직 함수]
# ==========================================

def display_menu() -> str:
    """메뉴를 출력하고 사용자의 선택을 반환합니다."""
    while True:
        print("\n--- 메인 메뉴 ---")
        for key, (title, _) in MENU_OPTIONS.items():
            print(f"{key}) {title}")
        
        choice = input(f'메뉴 선택(1 ~ {len(MENU_OPTIONS)}번)> ').strip()
        
        if choice in MENU_OPTIONS:
            return choice
        print('잘못된 입력입니다. 다시 선택해 주세요.')

def run_chat_session(curator: TravelCurator, prompt_message: str):
    """
    채팅 세션을 실행합니다.
    사용자가 'exit'이나 '0'을 입력하기 전까지 대화를 유지합니다.
    """
    print(f"\n[INFO] {prompt_message}")
    print(f"(메뉴 돌아가기: {CMD_BACK})")

    while True:
        user_input = input('\n사용자> ').strip()

        # 예외 처리: 입력값 확인
        if not user_input:
            continue
            
        # 뒤로 가기 로직
        if user_input == CMD_BACK:
            print("메인 메뉴로 돌아갑니다.")
            return

        # AI 응답 생성 및 출력
        try:
            response = curator.get_response(user_input)
            print(f"AI: {response}")
        except Exception as e:
            print(f"[Error] 응답 생성 중 오류 발생: {e}")

def main():
    """메인 실행 함수"""
    # AI 큐레이터 인스턴스 생성
    travel_curator = TravelCurator()

    while True:
        # 메뉴 선택
        selected_menu_id = display_menu()

        # 선택에 따른 분기 처리
        if selected_menu_id == '1':
            # 채팅 시작
            welcome_msg = MENU_OPTIONS['1'][1]
            run_chat_session(travel_curator, welcome_msg)
            
        elif selected_menu_id == '2':
            # 프로그램 종료
            print(MENU_OPTIONS['2'][1])
            sys.exit(0)

if __name__ == "__main__":
    main()