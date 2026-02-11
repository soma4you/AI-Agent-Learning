from sentence_transformers import SentenceTransformer
from PIL import Image
import faiss
import numpy as np
import os
from pathlib import Path # 파일 경로 처리

# model = SentenceTransformer('clip-Vit-B-32')
# path = os.path.dirname(os.path.abspath(__file__))
# print(f"Current path: {path}")

# image_folder = os.path.join(path, 'images')
# print(f"Image folder path: {image_folder}")

# image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
# print(f"Found {len(image_files)} images.")

# vectors = model.encode([image])
# vectors.astype('float32')
# dimension = vectors.shape[1]

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

query_text = "a cute cat"
text_vector = model.encode([query_text])
text_vector = text_vector.astype(np.float32) # FAISS는 float32 타입의 벡터를 사용하기 때문에 변환
distences, indices = index.search(text_vector, k=1) # k는 검색할 상위 개수

print("Distances: ", distences)
print("Indices: ", indices)




