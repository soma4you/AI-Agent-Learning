import whisper
import base64
from pathlib import Path
from PIL import Image
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# -------------------------------------------------------------------------
# 1. 설정 및 데이터 준비
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
AUDIO_PATH = BASE_DIR / 'audio' / 'cat.mp3'
IMAGE_PATH = BASE_DIR / 'images'

# 데이터 저장소 (텍스트와 이미지를 구분하여 관리할 수 있도록 구조 유지) - 데이터 셋
data_store = [
    {"id": 0, "type": "text", "content": "Information: This is a domestic cat sitting comfortably."},
    {"id": 1, "type": "text", "content": "Information: There is a golden retriever dog in the yard."},
    {"id": 2, "type": "text", "content": "Concept: AI and Machine Learning technologies."},    
    {"id": 3, "type": "text", "content": "Concept: Retrieval-Augmented Generation (RAG) system."},
]

image_paths = list(IMAGE_PATH.glob('*.jpg')) + list(IMAGE_PATH.glob('*.png'))
for path in image_paths:
    data_store.append({'id':len(data_store), 'type': 'image', 'path': path})

# -------------------------------------------------------------------------
# 2. STT - Whisper
# -------------------------------------------------------------------------
print(">>>>> [1/5] STT 변환 중...")
try:
    whisper_model = whisper.load_model("base")
    if not AUDIO_PATH.exists():
        raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {AUDIO_PATH}")
    
    stt_result = whisper_model.transcribe(str(AUDIO_PATH))
    user_question = stt_result['text'].strip()
    print(f" * 사용자 질문(STT): {user_question}")
except Exception as e:
    print(f"STT 오류/경고: {e}")
    # 테스트를 위해 강제 설정 (실제 구동시에는 STT 결과 사용)
    if not 'user_question' in locals() or not user_question:
        user_question = "Show me the cat information"

# -------------------------------------------------------------------------
# 3. Embedding & FAISS Indexing (분리 인덱싱)
# -------------------------------------------------------------------------
print(">>>>> [2/5] 모달리티별 분리 인덱싱 중...")
clip_model = SentenceTransformer('clip-ViT-B-32')

text_vectors = []
text_indices_map = []  # FAISS 인덱스 -> data_store ID 매핑

image_vectors = []
image_indices_map = [] # FAISS 인덱스 -> data_store ID 매핑

for item in data_store:
    if item['type'] == 'text':
        vec = clip_model.encode([item['content']], normalize_embeddings=True)
        text_vectors.append(vec)
        text_indices_map.append(item['id'])
        
    elif item['type'] == 'image':
        try:
            img = Image.open(item['path']).convert('RGB')
            # 사용자의 의도대로 '이미지 픽셀'을 임베딩
            vec = clip_model.encode([img], normalize_embeddings=True)
            image_vectors.append(vec)
            image_indices_map.append(item['id'])
        except Exception as e:
            print(f"이미지 로드 실패: {e}")


# ---------------------------------------------------------------------------------------------------------------
# WHY? 인덱스를 2개 설정한 이유!
# 원인 : '모달리티 간극(Modality Gap)'
# CLIP 모델을 사용할 때, 텍스트 질의("Show me...")는 
# 이미지의 픽셀 데이터(Visual Vector)보다 텍스트 데이터(Text Vector)와 훨씬 더 강한 유사도를 갖는 경향이 있습니다. 
# 특히 질문에 "Information" 같은 추상적인 단어가 포함되면, 내용은 달라도 형식이 비슷한 텍스트 문서들이 
# 이미지보다 더 높은 점수를 받기 쉽습니다.
# ---------------------------------------------------------------------------------------------------------------

# FAISS 인덱스 2개 생성 (텍스트용, 이미지용)
# 1. Text Index
if text_vectors:
    text_np = np.vstack(text_vectors).astype('float32')
    idx_text = faiss.IndexFlatIP(text_np.shape[1])
    idx_text.add(text_np)

# 2. Image Index
if image_vectors:
    image_np = np.vstack(image_vectors).astype('float32')
    idx_image = faiss.IndexFlatIP(image_np.shape[1])
    idx_image.add(image_np)

# -------------------------------------------------------------------------
# 4. 검색 (Hybrid Search)
# -------------------------------------------------------------------------
print(">>> [3/5] 관련 정보 검색 중 (Hybrid Search)...")

# 질문 벡터화
query_vector = clip_model.encode([user_question], normalize_embeddings=True).astype(np.float32)

final_indices = []

# 1) 텍스트에서 상위 2개 검색
if text_vectors:
    D_text, I_text = idx_text.search(query_vector, k=2)
    print(f" * 텍스트 검색 점수: {D_text[0]}")
    for idx in I_text[0]:
        if idx != -1:
            real_id = text_indices_map[idx]
            final_indices.append(real_id)

# 2) 이미지에서 상위 1개 검색
if image_vectors:
    D_img, I_img = idx_image.search(query_vector, k=2)
    print(f" * 이미지 검색 점수: {D_img[0]}")
    for idx in I_img[0]:
        if idx != -1:
            real_id = image_indices_map[idx]
            final_indices.append(real_id)

# 결과 수집
retrieved_texts = []
retrieved_images_b64 = []

print(f" * 최종 선택된 Data Store ID: {final_indices}")

for doc_id in final_indices:
    item = data_store[doc_id]
    
    if item['type'] == 'text':
        print(f" - [Text] {item['content'][:50]}...")
        retrieved_texts.append(item['content'])
        
    elif item['type'] == 'image':
        print(f" - [Image] {item['path']}")
        try:
            with open(item['path'], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                retrieved_images_b64.append(encoded_string)
        except Exception as e:
            print(f"이미지 인코딩 실패: {e}")

# -------------------------------------------------------------------------
# 5. LLM 답변 생성
# -------------------------------------------------------------------------
print(">>> [4/5] AI 답변 생성 중...")

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

context_str = "\n".join(retrieved_texts) if retrieved_texts else "텍스트 정보 없음"

system_prompt = f"""
당신은 멀티모달 AI입니다. 
사용자의 질문(오디오)에 대해 [Text Context]와 [Image]를 종합하여 답변하세요.
특히 이미지가 제공되었다면, 그 이미지의 시각적 특징을 설명에 포함하세요.
최종 결과물은 한국어로 출력!

[Text Context]
{context_str}
"""

messages_content = [{"type": "text", "text": user_question}]

# 이미지 추가
for b64_img in retrieved_images_b64:
    messages_content.append({
        "type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
    })

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=messages_content)
]

response = llm.invoke(messages)

print("\n" + "="*30)
print(f"* 최종 답변:\n{response.content}")
print("="*30)