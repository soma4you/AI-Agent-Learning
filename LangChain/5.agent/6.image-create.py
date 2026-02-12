import streamlit as st

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random

from datetime import datetime
def draw_card(text):

    # 도화지 (500 x 300 / 크림색 배경)
    img = Image.new("RGB", (500, 300), (255, 255, 255))
    draw = ImageDraw.Draw(img) # 그리기

    try:
        # 폰트 설정 (맑은고딕 or 궁서)
        font_path = Path("c:/windows/fonts/batang.ttc") if random.randint(1,2) == 1 else Path("c:/windows/fonts/malgun.ttf")
        font = ImageFont.truetype(str(font_path), 30)

    except:
        st.error("폰트를 찾을 수 없습니다.")
        font = ImageFont.load_default()

    draw.text((50, 30), f"오늘의 추천: {text}", font=font, fill=(255, 0, 0))
    draw.rectangle([10, 10, 490, 290], outline=(100, 100, 100), width=3)
    
    file_name = f"{datetime.now().strftime('%d_%H%M%S')}_{text}_card.png"
    img.save(file_name)
    return file_name

st.title('요리사 레시피 생성기')
st.write("요리사가 직접 손을 움직여 파일을 생성하는 단계입니다.")
menu = st.text_input("요리사에게 질문해보세요.(고등어 가격이 얼마인가요? 혹은 김치찌개 끓이 만드는 법)")
if st.button("요리 카드 제작"):
    if menu:
        with st.spinner("요리사가 요리 카드를 만들고 있습니다..."):
           path = draw_card(menu)
           st.image(path)
           st.download_button("요리 카드 다운로드", data=open(path, "rb").read(), file_name=path, mime="image/png")
           menu = ""
           Path(path).unlink(missing_ok=True)
    else:
        st.warning("메뉴 이름을 먼저 입력해주세요!")
    