from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
load_dotenv()

model = init_chat_model(
    model='gpt-4o-mini', 
    temperature = 0.7,  # 창의성(0.0 ~ 1.0)
    timeout = 10,       # 응답 대기 시간(초) - 무한 대기 방지
    max_tokens = 1000,  # 용량(응답 최대 길이 제한)
    max_retries = 1     # 안전성(자동 재시도 횟수)
)

# ----------------------------------
# batch() : 여러 질문을 병렬적으로 요청 가능 -> UX 증가 및 모델 호출을 줄여 비용 감소
# ----------------------------------
responses = model.batch(
    inputs = [
        'REST API란? 글자수 100자 이내',
        '인공지능이란? 글자수 100자 이내',
        '랭체인의 핵심 키워드 5개 추천'
    ]
)
for i, response in enumerate(responses):
    print(f'{i+1}) {response.text()}')
    print(f"{'-'*50}\n")

# -- 출력 결과 --
'''
1) REST API는 Representational State Transfer의 약자로, 웹 서비스와 클라이언트 간의 데이터 교환을 위한 아키텍처 스타일입니다. HTTP 프로토콜을 기반으로 하여, 자원(리소스)을 URI로 식별하고, CRUD(Create, Read, Update, Delete) 작업을 수행할 수 있습니다.
--------------------------------------------------

2) 인공지능(AI)은 인간의 지능을 모방하여 학습, 추론, 문제 해결 등의 기능을 수행하는 기술입니다. 머신러닝, 자연어 처리 등 다양한 분야에서 활용되어 자동화와 데이터 분석을 돕습니다.       
--------------------------------------------------

3) 랭체인(LangChain)의 핵심 키워드 5개는 다음과 같습니다:

1. **언어 모델** (Language Model) - 다양한 자연어 처리 작업을 수행하기 위해 사용하는 AI 모델.
2. **체인** (Chain) - 여러 단계의 처리를 연결하여 복잡한 작업을 수행하는 구조.
3. **프롬프트** (Prompt) - 모델에 입력하는 텍스트로, 원하는 출력을 유도하는 역할.
4. **데이터 소스** (Data Source) - 모델이 참고하거나 학습하는 데이터의 출처.
5. **API 통합** (API Integration) - 외부 서비스와의 연동을 통해 기능을 확장하는 과정.        

이 키워드들은 랭체인이 제공하는 기능과 구조를 이해하는 데 중요한 요소들입니다.
'''