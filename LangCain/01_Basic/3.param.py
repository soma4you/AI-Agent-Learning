# 모듈 불러오기
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# api_key 설정
import dotenv
dotenv.load_dotenv()

# 1. 모델 설정(필수)
model = ChatOpenAI(
    model='gpt-4o-mini', 
    temperature=0.9, # 창의성 = 0.0 ~ 2.0 (값은 llm 모델별 상이)
)

# 2. 프롬프트 설정(필수)
prompt = ChatPromptTemplate.from_template("다음 뉴스 내용을 바탕으로 사람들의 클릭을 유도하는 '낚시성' 헤드라인 3개를 만들어:{content}")
news_content = "애플이 새로운 AI 기능을 탑재한 아이폰 18을 내년에 출시한다고 발표했습니다."

# 3. 체인 생성 (LCEL의 핵심)
chain = prompt | model

# 4. request(요청)
response = chain.invoke({'content':news_content})
print(f"응답 결과 >>>\n{response}\n")
'''
응답 결과 >>>
content='1. "애플 아이폰 18, 구글을 제압할 AI 비밀 기능 공개! 당신의 스마트폰 사용이 변한다!"\n2. "아이폰 18 발표! 애플의 새로운 AI 기능이 당신의 일 상을 어떻게 뒤바꿀지 궁금하지 않나요?"\n3. "충격! 애플, 2024년 아이폰 18에 탑재된 AI 기능으로 모든 것을 바꾼다!"' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 96, 'prompt_tokens': 59, 'total_tokens': 155, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_1590f93f9d', 'id': 'chatcmpl-D5mab0cv1zK3wJnNuALDDqFgLNcgK', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='run--019c2c5c-936a-7aa2-85ab-301dc591703b-0' usage_metadata={'input_tokens': 59, 'output_tokens': 96, 'total_tokens': 155, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
'''

print(f"응답 결과(metadata) >>>\n{response.response_metadata}\n")
'''
응답 결과(metadata) >>>
{'token_usage': {'completion_tokens': 84, 'prompt_tokens': 59, 'total_tokens': 143, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_1590f93f9d', 'id': 'chatcmpl-D5mX7XMsOgLxMQiPdpGG68mmF9wYg', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}
'''

print(f"응답 결과(content) >>>\n{response.content}")
'''
응답 결과(content) >>>
1. "애플이 공개한 아이폰 18, 당신의 생각을 읽는 AI 기능이 탑재된다?!"
2. "충격! 아이폰 18, AI로 당신의 삶을 완전히 바꿀 준비 완료!"
3. "애플의 혁신! 아이폰 18에 숨겨진 AI 비밀 공개, 당신의 예상을 뒤엎는다!"
'''



