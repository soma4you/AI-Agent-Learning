from pathlib import Path                              # 파일 경로 처리
from PIL import Image                                 # 이미지 처리 라이브러리
import faiss                                          # 벡터 검색 라이브러리
import numpy as np                                    # 수치 계산 라이브러리
from sentence_transformers import SentenceTransformer # 텍스트 및 이미지 임베딩 모델

# 멀티 이미지 처리
#-------------------------------------------------------------------------
# -- 벡터 정규화 및 코사인 유사도 사용 --
# FAISS에서 코사인 유사도를 사용하려면, 
# 벡터를 정규화(Normalize) 한 뒤 반드시 **내적(Inner Product, IndexFlatIP)**을 사용


path = Path(__file__).parent / 'images'

# 1. 이미지 파일 경로 리스트 생성
image_paths = list(path.glob('*.jpg')) + list(path.glob('*.png')) # 이미지 파일 경로 리스트
print("Image paths: ", len(image_paths))

# 2. 이미지 로드 및 RGB 변환
images = [Image.open(path).convert('RGB') for path in image_paths] # 이미지 로드 및 RGB 변환

# 3. 이미지 임베딩
model = SentenceTransformer('clip-ViT-B-32') # 가성비 모델
# model = SentenceTransformer('clip-ViT-L-14') # 성능 좋은 모델
# model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1') # 다국어 지원 모델
image_embeddings = model.encode(images, normalize_embeddings=True) # 이미지 임베딩

# 4. 이미지 임베딩 확인
vector = image_embeddings.astype('float32') # FAISS는 float32 타입의 벡터를 사용하기 때문에
# faiss.normalize_L2(vector) # 벡터 정규화 (내적 인덱스 사용 시 필요)

# 5. FAISS 인덱스 생성 및 벡터 추가
dimension = vector.shape[1]          # 벡터의 차원
# index = faiss.IndexFlatL2(dimension) # L2 거리 기반의 벡터 검색 인덱스 생성
index = faiss.IndexFlatIP(dimension) # Inner Product(내적) 인덱스 사용
index.add(vector)                    # 벡터 추가

# 6. 텍스트 쿼리 벡터화
query = "a  cat"
query_vector = model.encode([query], normalize_embeddings=True).astype('float32') # 텍스트 쿼리를 벡터로 변환
# faiss.normalize_L2(query_vector) # 쿼리 벡터도 반드시 정규화!

# 7. 벡터(유사도) 검색 - 내적 값이 클수록 유사도가 높음
distances, indices = index.search(query_vector, k=2) # k는 검색할 상위 개수

print(f"결과: {'-' * 20}")
for p in indices[0]:
    print(f"가장 유사한 이미지: {image_paths[p].name}")
print(f"거리: {distances[0]}")

'''
distances가 
0.2 미만이라면, 데이터셋에 해당 이미지가 아예 없거나 모델이 전혀 이해하지 못하고 있다는 뜻입니다.
1.0에 가까울수록 매우 유사한 이미지입니다.
'''
# 검색된 이미지 열기
# similar_image = Image.open(image_paths[indices[0][0]])
# similar_image.show() # 검색된 이미지 출력


