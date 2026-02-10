# ---------------------------------
# 파일 경로 설정
# ---------------------------------
from pathlib import Path

base_path = Path(__file__).parent # 실행할 파이썬 파일의 경로
DATA_DIR = base_path / 'data'     # pdf 파일이 담길 폴더 경로 
file_name = 'Samsung_Card_Manual_Korean_1.3.pdf'


# ---------------------------------
# PDF 읽어오기
# ---------------------------------
from langchain_community.document_loaders import UnstructuredPDFLoader

loader = UnstructuredPDFLoader(DATA_DIR / file_name)
pages = loader.load() 


# ---------------------------------
# 텍스트 분할 도구
# ---------------------------------
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,     # 조각의 최대 길이
    chunk_overlap=50    # 조각 간의 중첩되는 영역
)
docs = splitter.split_documents(pages)


# ---------------------------------
# 문자열을 숫자로 바꿔주는 클래스
# ---------------------------------
from langchain_openai import OpenAIEmbeddings
embedding = OpenAIEmbeddings()
vector = embedding.embed_query('인공지능 에이전트란 무엇인가요?')
print(f'변환된 숫자의 벡터 길이: {len(vector)}')

# ---------------------------------
# 환경변수 로드
# ---------------------------------
from dotenv import load_dotenv

load_dotenv()

