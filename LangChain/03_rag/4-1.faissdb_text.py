from langchain_community.vectorstores import FAISS   # 벡터 저장소 도구 (FAISS)
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 문서 분할 도구
from langchain.docstore.document import Document  # 문서 객체

from langchain_openai import OpenAIEmbeddings # OpenAI 임베딩 모델(권장)
# from langchain_community.embeddings import OpenAIEmbeddings  # OpenAI 임베딩 모델(레거시)

# 1. 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

raw_test = """
FAISS는 Facebook AI Research에서 개발한 벡터 검색 라이브러리입니다.
대규모 백터 데이터에서 빠른 최근접 이웃 검색을 지원합니다.
LangChain은 FAISS을 활용하여 문서 검색 및 질문 응답 시스템을 구축할 수 있습니다.
"""

# 2. 일정 길이로 쪼개기
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # chunk 길이
    chunk_overlap=20 # 1/5
)
print(f'text_splitter>>> \n{text_splitter}')
# <langchain_text_splitters.character.RecursiveCharacterTextSplitter object at 0x0000020AA248B8B0>


docs = text_splitter.split_documents([
    Document(page_content=raw_test)
])
print(f'docs>>> \n{docs}')
# [Document(metadata={}, page_content='FAISS는 Facebook AI Research에서  개발한 벡터 검색 라이브러리입니다.\n대규모 백터 데이터에서 빠른 최근접  이웃 검색을 지원합니다.'), Document(metadata={}, page_content='LangChain 은  FAISS 을 활용하여 문서 검색 및 질문 응답 시스템을 구축할 수 있습니 다.')]

# 임베딩 모델 초기화 (텍스트 문자열 -> 숫자 벡터로 변환)
embeddings = OpenAIEmbeddings()
print(f'embeddings>>> \n{embeddings}')
# client=<openai.resources.embeddings.Embeddings object ...>

# 문서 조각들과 임베팅 모델을 합쳐서 FAISS 벡터 DB 생성
vector_db = FAISS.from_documents(docs, embeddings)
print(f'지식 창고(vector DB) 구축 완료')
print(f'vector_db>>> \n{vector_db}')
#  <langchain_community.vectorstores.faiss.FAISS object at 0x0000020AA48586D0>


# 5. 사용자가 질문을 던졌을 때 벡터DB에서 유사문서 검색
query = "FAISS는 무엇인가요?"
search_results  = vector_db.similarity_search(query=query, k=2)  # k=2 : 상위 2개 문서 검색
print(f'검색 결과>>> \n{search_results}')
# [Document(id='3c423b8a-8c7a-46a1-b37a-d63874995738', metadata={}, page_content='FAISS는 Facebook AI Research에서 개발한 벡터 검색 라이브러리입니다.\n대규모 백터 데이터에서 빠른 최근접 이웃 검색을 지원합니다.'), Document(id='aaf86abe-aee9-4241-b551-cd0f3d98e2fb', metadata={}, page_content='LangChain은  FAISS을 활용하여 문서 검색 및 질문 응답 시스템을 구축할  수 있습니다.')]

for i, result in enumerate(search_results, start=1):
    print(f'--- 검색 결과 {i} ---')
    print(result.page_content)
    
    # --- 검색 결과 1 ---
    # FAISS는 Facebook AI Research에서 개발한 벡터 검색 라이브러리입니다.     
    # 대규모 백터 데이터에서 빠른 최근접 이웃 검색을 지원합니다.

    # --- 검색 결과 2 ---
    # LangChain은  FAISS을 활용하여 문서 검색 및 질문 응답 시스템을 구축할 수 있습니다.
