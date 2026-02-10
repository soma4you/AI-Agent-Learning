from langchain_community.vectorstores import FAISS                  # 벡터 저장소 도구 (FAISS)
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 문서 분할 도구
from langchain.docstore.document import Document                    # 문서 객체
from langchain_openai import OpenAIEmbeddings                       # OpenAI 임베딩 모델(권장)

from dotenv import load_dotenv  # 환경변수 로드
load_dotenv()

import requests # 웹 페이지 요청 도구
from bs4 import BeautifulSoup as bs # HTML 파싱 도구
import re       # 정규표현식

url = "https://ko.wikipedia.org/wiki/인공지능"
raw_text = ''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 1. 웹 페이지에서 텍스트 추출
response = requests.get(url, headers=headers)
soup = bs(response.text, 'html.parser')
print(soup)

# 스크립트나 스타일 태그는 분석에 방해되므로 제거
for trash in soup(["script", "style", "aside", "footer", "header"]):
    trash.decompose()

# strip=True로 앞뒤 공백 제거, separator="\n"으로 태그 간 구분 명확화
clean_text = soup.get_text(separator="\n", strip=True)


# 연속된 줄바꿈이나 공백을 하나로 통합
refined_text = re.sub(r'\n+', '\n', clean_text)
refined_text = re.sub(r'[ \t]+', ' ', refined_text)


print(refined_text)
# raw_text = soup.get_text()
# # raw_text = raw_text.replace('\n\n', '\n').replace('\r', ' ').replace('\t', ' ')
# print(f'웹 페이지에서 추출한 원문>>> \n{raw_text[:500]}...')  # 앞 500자만 출력


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50 
)

docs = text_splitter.split_documents([
    Document(page_content=refined_text)
])

embeddings = OpenAIEmbeddings()

vector_db = FAISS.from_documents(docs, embeddings)
print(f'웹 크롤링 창고(vector DB) 구축 완료')


query = "인공지능이란 무엇인가?"
search_results  = vector_db.similarity_search(query=query, k=2)  # k=2 : 상위 2개 문서 검색
print(f'검색 결과>>> \n{search_results}')

for i, result in enumerate(search_results, start=1):
    print(f'--- 검색 결과 {i} ---')
    print(result.page_content[:300])