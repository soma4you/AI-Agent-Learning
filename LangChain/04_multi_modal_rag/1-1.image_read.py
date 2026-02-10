from pathlib import Path

import base64 # 이미지를 텍스트 형식으로 변환하기위해 사용
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

# 1. 이미지 파일을 읽어서 인코딩하는 함수
def encode_image(img_apth: Path | str):
    img_path = Path(img_apth)
    
    with img_path.open("rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
        
# 'local_stitch_terrarosa.jpg'
# 'building.png'

path = Path(__file__).parent / 'images' / 'local_stitch_terrarosa.jpg'
image_base64 = encode_image(path)

message = HumanMessage(content=[
    {
        "type": "text",
        "text": "이 이미지를 보고 무엇을 설명해줘."
    },
    {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{image_base64}"
        }
    }
])

response = model.invoke([message])
print(f'사진 분석 결과: {response.content}')