from langchain_core.runnables import RunnableParallel # 병렬 실행을 위한 RunnableParallel 임포트
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser   
from langchain_openai import ChatOpenAI

# OpenAI 챗 모델을 초기화합니다.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# {country} 의 수도를 물어보는 체인을 생성합니다.
chain1 = (
    PromptTemplate.from_template("{country} 의 수도는 어디야?")
    | model
    | StrOutputParser()
)

# {country} 의 면적을 물어보는 체인을 생성합니다.
chain2 = (
    PromptTemplate.from_template("{country} 의 면적은 얼마야?")
    | model
    | StrOutputParser()
)

# 위의 2개 체인을 동시에 생성하는 병렬 실행 체인을 생성합니다.
combined = RunnableParallel(capital=chain1, area=chain2)


# -------------------------------------------------------
# 단일 실행을 위한 예제
# -------------------------------------------------------
result1 = chain1.invoke({"country": "대한민국"})
print("대한민국의 수도:", result1)
# 대한민국의 수도: 대한민국의 수도는 서울입니다.


result2 = chain2.invoke({"country": "미국"})
print("미국의 면적:", result2)# 병렬 실행 체인을 호출하여 대한민국의 수도와 면적을 동시에 가져옵니다.
# 미국의 면적: 미국의 면적은 약 9,830,000 평방킬로미터(3,796,000 평방마일)입니다. 이는 미국이 세계에서 세 번째로 큰 나라임을 의미합니다.


result3 =combined.invoke({"country": "대한민국"})
print("대한민국의 수도와 면적:", result3["capital"], result3["area"])
# 대한민국의 수도와 면적: 대한민국의 수도는 서울입니다. 대한민국의 면적은 약 100,210 평방킬로미터입니다. 이는 한반도의 남쪽 부분에 해당하며, 북한과 함께 한반도를 구성하고 있습니다.


# -------------------------------------------------------
# 배치 처리를 위한 예제
# -------------------------------------------------------
result = chain1.batch([{"country": "대한민국"}, {"country": "미국"}])
print("배치 처리 결과:", result)
# 배치 처리 결과: ['대한민국의 수도는 서울입니다.', '미국의 수도는 워싱턴 D.C.입니다.']

result = chain2.batch([{"country": "대한민국"}, {"country": "미국"}])
print("배치 처리 결과:", result)
# 배치 처리 결과: ['대한민국의 면적은 약 100,210 평방킬로미 터(㎢)입니다. 이는 한반도의 남쪽에 위치한 지역으로, 북한과의 경계를 포함한 면적입니다.', '미국의 면적은 약 9,830,000 평방킬로미터(3,796,000 평방마일)입니다. 이는 미국이 세계 에서 세 번째로 큰 나라임을 의미합니다.']

result = combined.batch([{"country": "대한민국"}, {"country": "미국"}])
print("병렬 배치 처리 결과:", result)
# 병렬 배치 처리 결과: [{'capital': '대한민국의 수도는 서울 입니다.', 'area': '대한민국의 면적은 약 100,210 평방킬로미터입니다. 이는 한반도의 남쪽 부분에 해당하며, 북한과의 경 계를 포함한 전체 면적입니다.'}, {'capital': '미국의 수도는 워싱턴 D.C.입니다.', 'area': '미국의 면적은 약 9,830,000 평방킬로미터(3,796,000 평방마일)입니다. 이는 미국이 세계에서 세 번째로 큰 나라임을 의미합니다.'}]

