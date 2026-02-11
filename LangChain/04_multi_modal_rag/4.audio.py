import whisper # Whisper 모델 임포트
from pathlib import Path # 파일 경로 처리  

# Whisper 모델 로드
model = whisper.load_model("base")

# 오디오 파일 경로 설정
BASE_DIR = Path(__file__).parent / 'audio'
audio_path = BASE_DIR / '1.mp3'

print(f"오디오 파일 경로:{audio_path}")

# 음성 -> 텍스트 변환
result = model.transcribe((str(audio_path)))
print(f'음성 인식 결과: {result["text"]}')

