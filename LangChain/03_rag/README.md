# 🔍 LangChain RAG Basic

PDF 문서를 로드하고, 텍스트를 분할하여 벡터 DB를 구축하는 RAG (Retrieval-Augmented Generation) 파이프라인 기초 실습입니다.

## 📂 파일 목록

- **`1.read_pdf.py` / `1.readpdf.py`**:
  - `PyPDFLoader`를 사용하여 PDF 문서를 텍스트로 로드합니다.

- **`2.splittest.py`**:
  - `RecursiveCharacterTextSplitter`를 사용하여 긴 텍스트를 최적의 청크(Chunk) 단위로 분할합니다.

- **`3.text_embedding.py`**:
  - `OpenAIEmbeddings`를 사용하여 텍스트 데이터를 벡터화(Embedding)합니다.

- **`4-1.faissdb_text.py`**:
  - 텍스트 데이터를 기반으로 FAISS 벡터 저장소를 구축하고 유사도 검색(Similiarity Search)을 수행합니다.

- **`4-2.faissdb_web.py` / `4-3.faissdb_web.py`**:
  - 웹 페이지 콘텐츠를 크롤링하여 RAG 파이프라인에 통합하는 예제입니다.

- **`5.SamsungMemoryReaderPDF.py` / `6.SamsungMemoryReaderPDF.py`**:
  - 삼성전자 반도체 관련 PDF 문서를 로드하고 질의응답하는 실습입니다.

## 🚀 실행 방법

```bash
# 가상환경 활성화 후
python 4-1.faissdb_text.py
```
