# AI-Agent-Learning 🤖

AI 에이전트 개발과 데이터 분석, 웹 개발 학습 기록 저장소입니다.
날짜별로 진행한 학습 내용과 실습 코드를 정리하고 있습니다.

---

## 📚 프로젝트 개요

- **목표**: AI 에이전트, LLM, 웹 크롤링, 데이터 분석 등 다양한 분야의 실무 기술 습득
- **주요 주제**: Python, FastAPI, Streamlit, LLM 활용, 데이터 처리, 웹 개발
- **학습 기간**: 2025년 11월 ~ 현재

---

## 🛠️ 기술 스택

### 백엔드

- **Python**: 메인 프로그래밍 언어
- **FastAPI**: 고성능 웹 API 프레임워크
- **Flask**: 웹 애플리케이션 프레임워크
- **Streamlit**: 데이터 시각화 및 웹앱 프레임워크

### 데이터 처리

- **Pandas**: 데이터 프레임 처리
- **NumPy**: 수치 계산
- **Matplotlib, Seaborn**: 데이터 시각화
- **BeautifulSoup**: 웹 크롤링

### LLM & AI

- **LangChain**: LLM 애플리케이션 개발
- **Ollama**: 로컬 LLM 실행
- **OpenAI API**: GPT 활용

### 기타

- **MySQL**: 데이터베이스
- **SQLAlchemy**: ORM
- **Whisper**: 음성 인식
- **ChromaDB**: 벡터 DB

---

## 📅 2026년 학습 내용

### LangCain/02_Memory (2월 9일)

> Streamlit을 활용한 대화형 에이전트 및 RAG 기초

- **Streamlit 통합**: Streamlit을 활용하여 Chat Interface 구축 (`9.streamlit.py`, `10.userselect.py`)
- **Runnable & History**: `RunnableWithMessageHistory`를 활용한 대화 기록 관리 심화 (`7.runnalbewithchathistory.py`)
- **유틸리티**: TOML 설정 파일 관리 및 공통 함수 분리 (`8.convert_toml.py`, `callfunction.py`)

### LangCain/01_Basic & 02_Memory (2월 6일)

> LangChain 프롬프트 템플릿 및 메모리 시스템 기초

- **Prompt Template**: `PromptTemplate`, `ChatPromptTemplate` 활용 및 역할(Role) 설정 (`6.prompt.py`, `7.role.py`)
- **Memory System**:
  - **Stateless vs Stateful**: 체인 비교 (`1.nomemory.py`)
  - **Memory Types**: Buffer, Window, History Class 등 다양한 메모리 유형 실습
  - **Context Injection**: `MessagesPlaceholder` 활용

### LangCain/01_Basic (2월 5일)

> LCEL(LangChain Expression Language) 기초 및 활용

- **LCEL 기초**: 프롬프트, 모델, 파서 연결 및 체인 구성 (`1.LCEL.py`)
- **데이터 전달**: `invoke`를 통한 파라미터 전달 및 딕셔너리 활용 (`3.param.py`)
- **체인 결합**: 여러 체인을 연결하여 복합적인 로직 구현 (`4.combine.py`)
- **실습**: 번역 에이전트 구현 (`5.translation.py`)

### 2026_02/ch_260204 (2월 4일)

> Express 심화: Bootstrap, MongoDB 연동 및 파일 업로드

- **Bootstrap & EJS**: Bootstrap을 활용한 UI 구성 및 Express View Engine(EJS) 연동
- **MongoDB**: In-Memory 데이터 관리를 MongoDB로 마이그레이션 (Native Driver 사용)
- **File Upload**: 이미지 업로드 기능 구현 및 정적 파일 서빙 설정 (서버 모듈 분리)

### 2026_02/ch_260203 (2월 3일)

> 🤖 자동 코치 에이전트 (Agent Coach) 시뮬레이션

- **에이전틱 워크플로우**: [Plan → Execute → Verify] 구조의 에이전트 사고 흐름 구현
- **진단 프로세스**:
  - 규칙 기반 진단: 정규표현식을 활용한 실무 실수 패턴 분석
  - Trace 시스템: 에이전트의 내부 판단 과정을 단계별로그로 시각화
  - 상태 관리: 완료(DONE), 정보 부족(NEED_INFO), 실패(FAIL) 등의 상태 처리
- **환경 구성**: Node.js, Docker 환경에서의 과제 자동 진단 시뮬레이션

### 2026_02/ch_260202 (2월 2일)

> Docker CLI 및 Express 미들웨어/EJS 기초

- **Docker**: Docker CLI 가이드 및 컨테이너 관리 명령어 실습
- **Node.js**:
  - EJS 템플릿 엔진 기초 (데이터 전달, 제어문)
  - Express 미들웨어 (Middleware) 개념 및 활용
  - Express 애플리케이션 구조 및 라우팅 실습

### 2026_01/ch_260130 (1월 30일)

> Express와 EJS를 활용한 사용자 관리 CRUD 실습

- Express Framework를 활용한 RESTful 라우팅 구현 (GET, Redirect)
- EJS 템플릿 엔진을 활용한 데이터 바인딩 및 동적 리스트 생성
- 사용자 데이터 CRUD 기능 구현:
  - **Create**: 홈 화면에서 사용자 정보 입력 및 리스트 추가
  - **Read**: 사용자 전체 목록 조회 및 상세 정보 확인
  - **Update**: 기존 사용자 정보 수정 기능
  - **Delete**: 사용자 데이터 삭제 처리
- 인메모리(Memory) 배열을 활용한 데이터 상태 관리

### 2026_01/ch_260129 (1월 29일)

> Express와 EJS를 이용한 웹 서버 실습

- Express Framework 기초 설정
- EJS 템플릿 엔진을 활용한 동적 페이지 렌더링
- Query Parameter 처리 및 응답 페이지 구성

### 2026_01/ch_260128 (1월 28일)

> Streamlit을 이용한 웹 애플리케이션 개발

- **주제**: 챗봇/에이전트 웹 인터페이스 구현
- **파일**: `app.py`, `ex01.py`, `build_db.py`

### 2026_01/ch_260127 (1월 27일)

> MySQL TCL 기초, JavaScript Todo 앱

### 2026_01/ch_260126 (1월 26일)

> MySQL 조인 및 서브쿼리, JavaScript Todo 앱

### 2026_01/ch_260121 (1월 21일)

> Python 심화 학습

### 2026_01/ch_260109 (1월 9일)

> Flask를 이용한 멀티 기능 (계산기, 카운터, 채팅)

### 2026_01/ch_260108 (1월 8일)

> FastAPI AJAX 실습

### 2026_01/ch_260107 (1월 7일)

> Python 클래스 이론 및 테스트

### 2026_01/ch_260106 (1월 6일)

> FastAPI 기본 및 CRUD 실습

### 2026_01/ch_260105 (1월 5일)

> 웹 스크래핑 - 병렬 처리 및 성능 최적화

### 2026_01/ch_260102 (1월 2일)

> 데이터 시각화(Matplotlib), 뉴스 데이터 분석, HTML/CSS, Firebase 호스팅

---

## 📅 2025년 학습 내용

### 2025/ch_251231 (12월 31일)

> HTML/CSS/JavaScript 기초

### 2025/ch_251230 (12월 30일)

> 데이터 분석 및 시각화 (numpy, pandas, matplotlib, wordcloud), 웹 크롤링

### 2025/ch_251229 (12월 29일)

> 데이터 분석 기초

### 2025/ch_251226 (12월 26일)

> 데이터 처리

### 2025/ch_251224 (12월 24일)

> Python 기본 스크립트

### 2025/ch_251217

> LLM Function Calling 실습 (OpenAI GPT-4o, Streamlit)

### 2025/ch_251216

> 생성형 AI(LLM) 기초 실습, 프롬프트 엔지니어링

### 2025/ch_251215

> PDF 처리, STT(음성-텍스트 변환), 요약 파이프라인

### 2025/ch_251212

> LLM을 활용한 AI Agent 및 챗봇 구현

### 2025/ch_251211

> Streamlit을 이용한 AI Agent 데모

### 2025/ch_251210

> LLM 기반 구조화된 출력 처리

### 2025/ch_251209

> 로깅 시스템 및 채팅 기능

### 2025/ch_251208

> 프롬프트 기반 LLM 활용

### 2025/ch_251205

> 파일 처리 및 유틸리티

### 2025/ch_251204

> BeautifulSoup을 이용한 웹 크롤링

### 2025/ch_251203

> 다양한 데이터 처리 및 분석

### 2025/ch_251202

> 데이터 처리 및 분석 기초

### 2025/ch_251201

> Python 기본 학습

### 2025/ch*2511*

> 초기 프로젝트 및 연습 모음

---

## 🚀 빠른 시작

### 환경 설정

```bash
# Python 가상환경 생성 (권장)
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # macOS/Linux

# 패키지 설치
pip install -r requirements.txt
```

### 실행 예제

```bash
# Streamlit 앱 실행
streamlit run 2026_01/ch_260128/app.py

# FastAPI 실행
python -m uvicorn 2026_01/ch_260106.main:app --reload

# Python 스크립트 실행
python 2025/ch_251216/main.py
```

---

## 💡 주요 학습 내용

### AI & LLM

- LangChain을 이용한 에이전트 개발
- 다양한 LLM API 활용 (OpenAI, Ollama)
- 프롬프트 엔지니어링
- 벡터 DB와 임베딩

### 웹 개발

- FastAPI: 비동기 웹 API
- Flask: 전통적 웹 프레임워크
- Streamlit: 데이터 앱 구축
- JavaScript: 프론트엔드 상호작용

### 데이터 처리

- 웹 크롤링 (BeautifulSoup, Selenium)
- 데이터 정제 및 전처리
- 병렬 처리를 통한 성능 최적화
- 데이터 시각화

### 데이터베이스

- MySQL: 관계형 데이터베이스
- SQLAlchemy: ORM 패턴
- ChromaDB: 벡터 데이터베이스
- MongoDB: NoSQL 데이터베이스

---
