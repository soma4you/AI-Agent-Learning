# LangGraph: State Management & Workflow

LangGraph를 활용하여 상태 기반의 에이전트 워크플로우를 설계하고 구현하는 실습입니다.

## 📂 파일 목록

### 1. `1.plantest.py` (Basic StateGraph)

- **목표**: 가장 기초적인 StateGraph 구조 이해
- **구조**: 기획부(Planner) -> 제작부(Cook) -> 종료(End)
- **핵심**: `StateGraph`, `TypedDict`를 활용한 상태 정의 및 노드 연결

### 2. `2.payment.py` (Multi-Agent Linear Flow)

- **목표**: 3개 이상의 부서가 협업하는 선형적 워크플로우 구현
- **구조**: 기획부 -> 제작부 -> 검수부(Reviewer) -> 종료
- **핵심**: 다중 에이전트 간의 메시지 전달 및 역할 분담

### 3. `3.feedback.py` (Conditional Edges & Loops)

- **목표**: 조건에 따라 경로가 바뀌거나 되돌아가는(Loop) 워크플로우 구현
- **구조**:
  - 기획 -> 제작 -> 검수 -> (판단)
  - **Pass**: 종료 (Finish)
  - **Fail**: 제작부로 복귀 (Retry)
- **핵심**: `add_conditional_edges`, `should_continue` 함수를 통한 동적 라우팅

### 4. `7.parallel.py` (Custom Visualization)

- **목표**: 에이전트의 실행 경로(Execution Path)를 시각화하고 에러 복구 로직 강화
- **구조**: 기획 -> (조건부) 요리/에러 -> 검수 -> 종료
- **핵심**:
  - `PIL` 라이브러리를 활용한 커스텀 경로 그리기 (`draw_path_map`)
  - 점수(Score) 합산 및 에러 상태의 시각적 표현

### 5. `4.trace.py` (Execution Path Visualization)

- **목표**: 에이전트의 실행 경로(Execution Path)를 추적하고 시각화
- **구조**: 기획 -> 제작 -> 검수 -> 종료
- **핵심**:
  - `execution_path`를 State에 추가하여 방문한 노드 기록
  - `PIL`을 사용하여 노드 방문 순서대로 시각적 흐름도 생성

### 6. `5.score.py` (Scoring System)

- **목표**: 각 단계별 수행 결과에 대한 점수 산정 및 합산
- **구조**: 기획(10점) -> 제작(30점) -> 검수(60점) -> 종료
- **핵심**:
  - `scores` 리스트를 State에 추가하고 `operator.add`로 점수 누적
  - 최종 결과에서 총점 계산 및 시각화 포함

### 7. `6.fail-system.py` (Error Handling & Conditional Edges)

- **목표**: 에러 발생 시 처리 로직(Error Handler) 및 조건부 분기 구현
- **구조**: 기획 -> 제작 -> (성공: 검수 / 실패: 위기관리) -> 종료
- **핵심**:
  - `errors` 필드를 State에 추가하여 에러 메시지 관리
  - `add_conditional_edges`를 사용하여 에러 유무에 따라 다음 단계 동적 결정
  - 에러 발생 시 붉은색 텍스트로 시각화하여 문제 상황 직관적 표현
