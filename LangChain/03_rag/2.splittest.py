# ---------------------------------
# 파일 경로 설정
# ---------------------------------
from pathlib import Path

base_path = Path(__file__).parent # 실행할 파이썬 파일의 경로
DATA_DIR = base_path / 'data'     # pdf 파일이 담길 폴더 경로 
file_name = 'Samsung_Card_Manual_Korean_1.3.pdf'


# ---------------------------------
# PDF 읽어오기
# pip install "unstructured[all-docs]"
# ---------------------------------
from langchain_community.document_loaders import UnstructuredPDFLoader

loader = UnstructuredPDFLoader(DATA_DIR / file_name)
pages = loader.load() 

'''
# UnstructuredPDFLoader에서 페이지 수가 예상과 다르게 나오는 이유>
- 주로 텍스트 추출 방식과 전략(strategy) 설정 때문
# 해결을 위한 체크리스트>
- 모드 설정 확인: 기본적으로 Unstructured는 전체 문서를 하나의 Document 객체로 합치는 경우가 많음
  페이지별로 나누려면 mode="elements" 설정을 시도
- 분할 전략(Strategy): strategy="fast"는 텍스트만 대충 긁어옴
  strategy="hi_res"는 정확한 페이지 구분 및 복잡한 레이아웃 로드 가능
- 라이브러리 특성: Unstructured는 PDF의 물리적 페이지 번호보다 텍스트의 논리적 구조를 중시
  물리적 페이지가 중요하다면 PyPDFLoader를 사용하는 것이 훨씬 정확함
'''
print(f"총 페이지 수: {len(pages)}쪽")
print(f"1페이지 미리보기: {pages[0].page_content[:200]}") # 첫페이지 200자만 출력



# ---------------------------------
# 텍스트 분할 도구
# ---------------------------------
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,     # 조각의 최대 길이 (일반적으로 500~1000자 설정)
    chunk_overlap=50    # 조각 간의 중첩되는 영역 : 앞 조각의 마지막 내용 일부를 뒤 조각에 포함시켜 문맥이 끊기는 것을 방지
)
docs = splitter.split_documents(pages)



# ---------------------------------
# 문자열을 숫자로 바꿔주는 클래스
# ---------------------------------
from langchain_openai import OpenAIEmbeddings
embedding = OpenAIEmbeddings()
vector = embedding.embed_query('인공지능 에이전트란 무엇인가요?')
print(f'변환된 숫자의 벡터 길이: {len(vector)}')

