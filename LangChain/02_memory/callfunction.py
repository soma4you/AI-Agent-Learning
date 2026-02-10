'''
공통 import 및 환경 설정 모듈
    이 파일을 import 하시면
    1) .env 자동로드
    2) 필요한 클래스들을 함께 가져올 수 있음
'''

# 모듈 실습
# 자주 사용되거나 중복이 있는 구문이 있다면 따로 모아서 도구처럼 사용
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

