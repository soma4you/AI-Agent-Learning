from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 그 다음 로더를 불러오세요
from langchain_community.document_loaders import AsyncHtmlLoader


# 1. 데이터 로드 (위키백과)
url = "https://ko.wikipedia.org/wiki/인공지능"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

loader = AsyncHtmlLoader([url], header_template=headers)
docs = loader.load()

# 2. 데이터 정제: tags_to_extract 사용
# p(문단), h2/h3(제목) 태그만 추출하여 핵심 내용만 남김
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(
    docs, 
    tags_to_extract=["p", "h2", "h3"]
)

# 3. 텍스트 분할 (RecursiveCharacterTextSplitter)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs_transformed)

# 4. 벡터스토어 생성 및 검색기(Retriever) 설정
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# 5. 프롬프트 및 체인 생성
template = """다음 문맥을 이용하여 질문에 답하세요. 
답변을 모르면 모른다고 하고 근거 없는 말을 지어내지 마세요.

문맥: {context}

질문: {question}
답변:"""

prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4o-mini")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 6. 실행
question = "인공지능의 기본 개념이 뭐야?"
response = rag_chain.invoke(question)

print(f"--- 질문: {question} ---")
print(response)
