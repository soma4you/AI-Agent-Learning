# 모듈 불러오기
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# api_key
import dotenv
dotenv.load_dotenv()

# 1. 모델 설정(필수)
model = ChatOpenAI(model='gpt-4o-mini')
print("model=> ", model) # 객체생성 => 메모리에 공간 생성 => 주소값

# 2. 프롬프트 설정(필수)
prompt = ChatPromptTemplate.from_template('인공지능 대해 짧게 한 문장으로 설명해')   # (1)
#prompt = ChatPromptTemplate.from_template('{topic}에 대해 짧게 한 문장으로 설명해') # (2)

# 3. 파서 설정(모델의 응답값 중에서 문자열만 쏙 뽑아냄)
parser = StrOutputParser() # 객체생성

# 4. 체인 생성 (LCEL의 핵심)
chain = prompt | model # parser (생략 가능) (1)
# chain = prompt | model | parser         # (2)

# 5. 실행 (입력 데이터는 딕셔너리 형태로 전달)
result = chain.invoke({})                     # (1)
#result = chain.invoke({'topic':'인공지능'})  # (2)

print(f"응답 결과 >>>\n{result}")
'''응답 결과(1) >>>
content='인공지능은 기계가 인간의 지능을 모방하여 학습, 문제 해결, 언어 이해 등의 작업을 수행할 수 있도록 하는 기술입니다.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 35, 'prompt_tokens': 20, 'total_tokens': 55, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_1590f93f9d', 'id': 'chatcmpl-D5muOXHGCJPpHHKnOVRAsIZWKtJ9L', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='run--019c2c6f-4a29-70d0-b8e0-bd4d753fdf68-0' usage_metadata={'input_tokens': 20, 'output_tokens': 35, 'total_tokens': 55, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
'''

print(f"응답 결과 >>>\n{result.content}")
'''응답 결과(1) >>>
인공지능은 기계가 인간의 지능을 모방하여 학습, 문제 해결, 의사 결정 등을 수행할 수 있도록 하는 기술입니다.
'''

# print(f"응답 결과 >>>\n{result}\n") # (2)
# '''응답 결과(2) >>>
# 인공지능은 기계가 인간의 지능을 모방하여 학습, 문제 해결, 의사 결정 등을 수행할 수 있도록 하는 기술입니다.
# '''