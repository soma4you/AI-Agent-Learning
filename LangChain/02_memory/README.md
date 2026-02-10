# 📅 2026년 2월 6일 LangChain 실습 - Memory & Prompt

이 디렉토리는 LangChain의 **PromptTemplate** 활용과 다양한 **Memory** 기능을 실습한 예제 코드를 포함하고 있습니다.

## 📂 파일 목록 및 설명

### 1. 01_Basic (기초)

이전 디렉토리(`../01_Basic`)에 추가된 파일들입니다.

- **[6.prompt.py](../01_Basic/6.prompt.py)**: `PromptTemplate`을 사용하여 입력 변수를 템플릿에 삽입하는 기본 예제.
- **[7.role.py](../01_Basic/7.role.py)**: `SystemMessage`, `HumanMessage`, `AIMessage`를 활용하여 역할(Role) 기반의 대화를 구성하는 방법.
- **[8.multi_chat.py](../01_Basic/8.multi_chat.py)**: 여러 번의 대화를 주고받는 멀티턴(Multi-turn) 구조의 기초 구현.

### 2. 02_Memory (현재 디렉토리)

LangChain의 다양한 메모리 구현 방식을 다룹니다.

- **[1.nomemory.py](./1.nomemory.py)**: 메모리 기능이 없는 상태 비저장(Stateless) 체인 예제. 이전 대화를 기억하지 못함.
- **[2.history.py](./2.history.py)**: `ChatMessageHistory`를 사용하여 대화 내용을 수동으로 저장하고 관리하는 방법.
- **[3.messageplaceholder.py](./3.messageplaceholder.py)**: `MessagesPlaceholder`를 사용하여 프롬프트 내에 대화 기록이 들어갈 위치를 지정하는 방법.
- **[4.chatmessagehistory.py](./4.chatmessagehistory.py)**: 대화 기록을 관리하는 클래스의 심화 활용법.
- **[5.fullmemorysave.py](./5.fullmemorysave.py)**: `ConversationBufferMemory`를 사용하여 전체 대화 내용을 저장하고 체인에 전달하는 방법.
- **[6.windowmemory.py](./6.windowmemory.py)**: `ConversationBufferWindowMemory`를 사용하여 최근 N개의 대화만 기억(Windowing)하는 효율적인 메모리 관리 방법.
