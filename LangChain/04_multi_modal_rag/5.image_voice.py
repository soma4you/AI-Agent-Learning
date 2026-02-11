import whisper
from pathlib import Path

from PIL import Image
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# -------------------------------------------------------------------------
# STT - Whisper
# -------------------------------------------------------------------------
whisper_model = whisper.load_model("base")

# 오디오 파일 경로 설정
BASE_DIR = Path(__file__).parent / 'audio'
audio_path = BASE_DIR / 'cat.mp3'

# print(f"오디오 파일 경로:{audio_path}")

# 음성 -> 텍스트 변환 (STT)
stt_result = whisper_model.transcribe((str(audio_path)))
stt_text = stt_result['text'].strip()
# print(f'\n*STT 결과: {stt_text}')


# -------------------------------------------------------------------------
# RAG - CLIP + FAISS
# -------------------------------------------------------------------------
clip_model = SentenceTransformer('clip-ViT-B-32')

# 텍스트 데이터셋
documents = [
    "Information: This is a domestic cat sitting comfortably.",  # 고양이에 대한 설명
    "Information: There is a golden retriever dog in the yard.", # 강아지에 대한 설명
    "Concept: AI and Machine Learning technologies.",            # AI 기술 설명
    "Image: Cute cat image.",                                    # 이미지 설명
    "Concept: Retrieval-Augmented Generation (RAG) system."      # RAG 시스템 설명
]

# 이미지 데이터셋
image_path = Path(__file__).parent / 'images' / 'cat.jpg'
image = Image.open(image_path).convert('RGB') # 이미지 로드 및 RGB 변환

# 텍스트 벡터화 
text_vector = clip_model.encode(documents, normalize_embeddings=True).astype('float32') # 텍스트 쿼리를 벡터로 변환
faiss.normalize_L2(text_vector) # 쿼리 벡터도 반드시 정규화!

# 이미지 벡터화
image_vector = clip_model.encode([image], normalize_embeddings=True).astype('float32') 
faiss.normalize_L2(image_vector) # 벡터 정규화 (내적 인덱스 사용 시 필요)

# 벡터화 합치기
all_vectors = np.vstack((text_vector, image_vector))
faiss.normalize_L2(all_vectors) # 벡터 정규화 (cosine similarity 목적)


# FAISS 저장소(인덱스) 생성 및 벡터 추가
dimension = all_vectors.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(all_vectors)

# -------------------------------------------------------------------------
# 유사도 검색 및 결과 출력
# -------------------------------------------------------------------------

# 연관 정보 찾기 -> 사용자 음성 질물을 검색을 위한 숫자 벡터화
query_vector = clip_model.encode([stt_text], normalize_embeddings=True).astype(np.float32)
faiss.normalize_L2(query_vector)

# 질문과 가장 닮은 상위 3개 검색
distances, indices = index.search(query_vector, k=3)

# 검색된 결과(인덱스 번호)를 실제 내용으로 매칭
print(f"검색된 인덱스들: {indices[0]}")
print(f"각 결과와의 거리: {distances[0]}")


retriever_contents =[]
for idx in indices[0]:
    print(f"검색된 결과 수idx: {idx}")
    
    if idx < len(documents):
        retriever_contents.append(documents[idx])
    elif idx == len(documents):
        # 찾은 번호가 4번 (이미지 벡터)라면 이미지 설명 추가
        print(f"찾은 이미지 인덱스: {idx}")
        retriever_contents.append("Visual Data: A high-resolution photo of a cat from 'cat.jpg'")        
    
# 찾아낸 여러 정보들을 줄바꿈으로 연결해 하나의 참고 자료 만들기
context_text = "\n".join(retriever_contents)
print(f"\n*검색된 참고 자료:\n{context_text}")


template = '''
당신은 멀티모달 정보를 처리해주는 전문가 AI 어시스턴트입니다.
제공된 [context]에는 텍스트 정보뿐만 아니라 이미지 파일에 대한 설명(Visual Data)도 포함되어 있습니다.
사용자의 질문인 [question]과 가장 연관성이 높은 정보를 [context]에서 찾아 상세히 한국어로 답변해주세요.

[context]
{context}

[question]
{question}

[answer]

'''.strip()


llm = ChatOpenAI(model='gpt-4o-mini')
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm | StrOutputParser()

response = chain.invoke({'question':stt_text, 'context': context_text})

print(f"\n*최종 답변:\n{response}")
