from sentence_transformers import SentenceTransformer # 멀티 모달 임베팅 모델 로드
from PIL import Image # 이미지 파일 열기
import faiss # 벡터 검색 라이브러리
import numpy as np # 수치 계산 라이브러리(벡터 검색용)
from pathlib import Path # 파일 경로 처리

# 1. 이미지 파일 경로 설정
path = Path(__file__).parent / 'images'

# 2. CLIP 멀티모달 모델 로드
model = SentenceTransformer('clip-ViT-B-32')

# 3. 이미지 로드
image = Image.open(path / 'cat.jpg').convert('RGB')

# 4. 이미지 임베딩
image_embedding = model.encode([image])

# 5. 벡터 검색 (FAISS는 float32 타입의 벡터를 사용하기 때문에 변환)
vector = image_embedding.astype(np.float32)

# 6. 벡터 검색 인덱스 생성
dimestion = vector.shape[1] # 벡터의 차원
index = faiss.IndexFlatL2(dimestion) # L2 거리 기반의 벡터 검색 인덱스 생성
index.add(vector) # 벡터 추가

# 7. 벡터 검색
print("Vector shape: ", vector.shape) # 벡터의 차원
print("Index shape: ", index.ntotal)  # 인덱스의 크기

# RAG의 한계
# 실시간으로 변경되는 데이터에 대한 대응이 어렵다.
# 원본 소스의 부분 업데이트시 전체를 다시 색인해야한다.


#pip install --upgrade setuptools wheel
#pip install setuptools

