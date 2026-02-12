import streamlit as st
from PIL import Image, ImageDraw, ImageFont

from pathlib import Path
from datetime import datetime

if "my_frige" not in st.session_state:
    st.session_state.my_frige = {'img': None, 'menu': None}

st.title("📥 요리사의 신선 보관함 실습")
st.write("버튼을 눌러도 데이터가 사라지지 않는 '금고'의 원리를 배웁니다.")

menu = st.text_input("냉장고에 넣을 메뉴 이름을 입력하세요:")
if st.button("요리 완성 및 냉장고 보관"):
    if menu:
        img = Image.new("RGB", (400, 200), color=(255, 255, 200))
        draw = ImageDraw.Draw(img) 

        try:
            # 폰트 설정 (궁서)
            font_path = Path("c:/windows/fonts/batang.ttc")
            font = ImageFont.truetype(str(font_path), 30)

            draw.text((50, 30), f"오늘의 추천: {menu}", font=font, fill=(255, 0, 0))
            draw.rectangle([10, 10, 490, 290], outline=(100, 100, 100), width=3)
            
            file_name = Path(f"{datetime.now().strftime('%d_%H%M%S')}_{menu}_card.png")
            img.save(file_name)

            with file_name.open("rb") as f:
                st.session_state.my_frige['img'] = f.read()
                st.session_state.my_frige['menu'] = menu
        except:
            st.error("폰트를 찾을 수 없습니다.")
            font = ImageFont.load_default()
        
        st.success(f"{menu} 메뉴가 냉장고에 추가되었습니다.")

if st.session_state.my_frige['img'] is not None:
    st.divider()
    st.subheader(f"냉장고에서 꺼낸 요리: {st.session_state.my_frige['menu']}")
    st.image(st.session_state.my_frige['img'])
    st.download_button("냉장고에서 꺼낸 요리 저장", data=st.session_state.my_frige['img'], file_name=f"{st.session_state.my_frige['menu']}_card.png", mime="image/png")
