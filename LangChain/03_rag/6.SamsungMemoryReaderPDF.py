from langchain_community.document_loaders import PyPDFLoader # PDF 문서 로더
from langchain.text_splitter import RecursiveCharacterTextSplitter # 문서 분할 도구
from langchain_openai import ChatOpenAI,OpenAIEmbeddings # OpenAI 임베딩 모델(권장)
from langchain_community.vectorstores import FAISS # 벡터 저장소 도구 (FAISS)
from langchain.docstore.document import Document ## 문서 객체
from langchain_core.runnables import RunnablePassthrough # 패스스루 러너 (입력=출력)
from langchain_core.prompts import ChatPromptTemplate # 채팅 프롬프트 템플릿

from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
path = Path(__file__).parent / "data" / "Samsung_Card_Manual_Korean_1.3.pdf"

loader = PyPDFLoader(path)

documents = loader.load() # List[Document]

# 문서 분할 객체
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50 
)

# 문서 분할
docs = text_splitter.split_documents(documents)

vector_db = FAISS.from_documents(docs, OpenAIEmbeddings())
print(f'PDF 문서 창고(vector DB) 구축 완료')

retriever = vector_db.as_retriever(search_Kwargs={"k":2}) # k=2 : 상위 2개 문서 검색
# vector_db.similarity_search(query="삼성카드 고객센터 번호가 뭐야?", k=2) # k=2 : 상위 2개 문서 검색

prompt = ChatPromptTemplate.from_template(
    '''
    당신은 삼성전자 메모리카드 메뉴얼을 작성한 전문가입니다.
    다음의 참고 문서를 바탕으로 질문에 정확하게 답변해 주세요.
    
    [참고문헌]
    {context}
    
    [질문]
    {question}
    
    제한사항: 한글로 간결하게 답변하세요.
    '''
)

rag_chain = (
    {'context': retriever, 'question': RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model='gpt-4o-mini', temperature=0)
)

# gpt-4o-mini 모델에게 물어보게 (1.지본지식(빨강) vs 검색을 통한 지식을 활용 RAG(파랑))
llm_base = ChatOpenAI(model='gpt-4o-mini', temperature=0)

RED = "\033[91m"  # 빨강: 기본 지식
BLUE = "\033[94m" # 파랑: RAG 활용
RESET = "\033[0m" # 초기화

# 테스트에 사용할 질물 리스트 준비
questions = [
    "삼성 메모리카드/UFD 인증 유틸리티에서 동시에 지원하는 최대 카드 수는?",
    "삼성 메모리카드/UFD 인증 유틸리티는 BitLocker가 활성화된 장치나 포멧되지 않은 장치를 인증할 수 있나?",
    "삼성 메모리카드/UFD 인증 유틸리티에서 지원되는 운영체제(OS) 버전은 무엇인가?)",
    "삼성 메모리카드/UFD 인증 유틸리티에서 정확한 인증 결과를 도출하지 못하게 만드는 원인 중 하나로 명시된 상황은 무엇입니까?",
    "삼성 메모리카드/UFD 인증 유틸리티가 공식적으로 지원하는 언어 구성으로 옳은 것은 무엇입니까?",
    "삼성 메모리카드/UFD 인증 유틸리티를 통해 인증이 불가능한 제품 상태나 유형은 무엇입니까?"
]

for i, q in enumerate(questions, start=1):
    base_answer = llm_base.invoke(q)
    rag_answer = rag_chain.invoke(q)
    
    print(f'--- 질문 {i} ---')
    print(f'{q}\n')
    print(f'{RED}[기본 지식 답변]{RESET}\n{base_answer.content}\n')
    print(f'{BLUE}[RAG 활용 답변]{RESET}\n{rag_answer.content}\n')
    print('============================\n')

# pip install torch==2.3.1 -f https://download.pytorch.org/whl/cpu/torch_stable.html

# pip install "transformers==4.41.2"

# pip install "scikit-learn==1.5.1"

# pip install "sentence-transformers==2.6.1"

# pip check (호환성 체크할것)

# No broken requirements found.

# => 설치하신 4개 모듈은 멀티모달 RAG / 임베딩 시스템의 핵심 스택

# ##########################이것은 아직 설치하지 마세요######################
# pip install git+https://github.com/openai/CLIP.git
# pip install torchvision==0.18.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu
# pip install ftfy==6.3.1
# #######################################################################