from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
load_dotenv()

model = init_chat_model(model='gpt-4o-mini')

# ----------------------------------
# invoke() : 답변(텍스트) 생성
# ----------------------------------
result = model.invoke(input='안녕하세요. 저는 홍길동입니다.')

print(result)
# -- 출력 결과 --
# content='안녕하세요, 홍길동님! 어떻게 도와드릴까요?' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 15, 'prompt_tokens': 16, 'total_tokens': 31, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_194c0b7559', 'id': 'chatcmpl-D7NNJ9XSSJGvxzVQ3YaPacKdLg6AM', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='run--019c42fe-cbb1-7bd3-a007-4ad3b8244c7e-0' usage_metadata={'input_tokens': 16, 'output_tokens': 15, 'total_tokens': 31, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

print(result.content)
# -- 출력 결과 --
# 안녕하세요, 홍길동님! 어떻게 도와드릴까요?

print(result.response_metadata)
# -- 출력 결과 --
# {'token_usage': {'completion_tokens': 15, 'prompt_tokens': 16, 'total_tokens': 31, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_194c0b7559', 'id': 'chatcmpl-D7NNJ9XSSJGvxzVQ3YaPacKdLg6AM', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}

print(result.usage_metadata)
# -- 출력 결과 --
# {'input_tokens': 16, 'output_tokens': 15, 'total_tokens': 31, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}