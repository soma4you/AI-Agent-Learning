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

query = '이 유틸리티는 동시에 몇 개의 메모리카드나 UFD(usb flash drive)를 지원합니까?'
answer = rag_chain.invoke(query)
print(f'질문: {query}\n')
print(f'답변: {answer.content}')