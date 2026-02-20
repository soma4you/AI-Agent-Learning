# -------------------------------------------------------
from langchain_community.vectorstores import FAISS                  # 벡터 저장소 도구 (FAISS)
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 문서 분할 도구
from langchain.docstore.document import Document                    # 문서 객체
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# -------------------------------------------------------
import requests                     # 웹 페이지 요청 도구
from bs4 import BeautifulSoup as bs # HTML 파싱 도구
import re                           # 정규표현식

# -------------------------------------------------------
from fastapi import FastAPI
from pydantic import BaseModel

# -------------------------------------------------------
from dotenv import load_dotenv  # 환경변수 로드
load_dotenv()


app = FastAPI()

embeddings = OpenAIEmbeddings()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_completion_tokens=1000,
    max_retries=5
)




def build_vector_db(url:str):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # 1. 웹 페이지에서 텍스트 추출
    response = requests.get(url, headers=HEADERS)
    soup = bs(response.text, 'html.parser')
    
    # 스크립트나 스타일 태그는 분석에 방해되므로 제거
    for trash in soup(["script", "style", "aside", "footer", "header", "a"]):
        trash.decompose()
    
    # strip=True로 앞뒤 공백 제거, separator="\n"으로 태그 간 구분 명확화
    clean_text = soup.get_text(separator="\n", strip=True)
    
    # 연속된 줄바꿈이나 공백을 하나로 통합
    refined_text = re.sub(r'\n+', '\n', clean_text)
    refined_text = re.sub(r'[ \t]+', ' ', refined_text)
    
    print(refined_text)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50 
    )
    
    docs = splitter.split_documents([
        Document(page_content=refined_text)
    ])

    vector_db = FAISS.from_documents(docs, embeddings)
    print(f'*** VectorDB > {vector_db}')
    print(f'웹 크롤링 창고(vector DB) 구축 완료')
    return vector_db


# 서버 시작시 벡터 DB 생성
vector_db = build_vector_db(url="https://ko.wikipedia.org/wiki/인공지능")

class QuestionRequest(BaseModel):
    question:str # 질문
    
class QuestionResponse(BaseModel):
    answer:str

@app.post("/ask", response_model=QuestionResponse)
def question(request: QuestionRequest):
    query = request.question
    results  = vector_db.similarity_search(query=query, k=2)  # k=2 : 상위 2개 문서 검색
    
    context = "\n\n".join(doc.page_content for doc in results)
    
    prompt = ChatPromptTemplate.from_template(
        """
        당신은 AI 전문가 입니다.
        반드시 아래 문서를 참고해서 답변하며, 문서에 없는 내용은 **모른다**고 하세요.
        
        문서:
        {context}
        
        질문:
        {question}
        """.strip()
    )
    
    chain = prompt | llm
    
    response = chain.invoke(input={
        "context":context,
        "question": query
    })

    return {"answer": response.content}