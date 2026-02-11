# 👁️ Multi-Modal RAG

텍스트와 이미지 데이터를 결합하여 벡터 검색을 수행하는 멀티모달 RAG (Retrieval-Augmented Generation) 실습입니다.

## 📂 파일 목록

- **`1-1.image_read.py`**:
  - `PIL` 라이브러리를 사용하여 이미지를 로드하고 정보를 확인하는 기본 예제입니다.

- **`1-2.image_rag.py`**:
  - `SentenceTransformer('clip-ViT-B-32')` 모델을 사용하여 이미지와 텍스트를 임베딩합니다.
  - `FAISS` 벡터 저장소를 구축하고, 이미지를 포함한 질문에 대해 가장 유사한 이미지를 검색합니다.

## 🚀 실행 방법

```bash
# 가상환경 활성화 후
python 1-2.image_rag.py
```
