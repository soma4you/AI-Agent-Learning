from callfunction import *
import streamlit as st

api_key = st.secrets['OPENAI_API_KEY']

llm = ChatOpenAI(model='gpt-4o-mini', api_key=api_key)
prompt = PromptTemplate.from_template('{topic} 주제에 대해서 설명해줘')
chain = prompt | llm | StrOutputParser()

# Streamlit UI
st.set_page_config(page_title='랭체인', page_icon='😁', layout='centered')
st.title('챗봇')

if 'messages' not in st.session_state:
    st.session_state.messages = []

# -- 입력 처리 함수 정의 --
def process_input():
    user_text = st.session_state.input_box.strip()
    if user_text:        
        st.session_state.messages.append(('user', user_text))
        st.session_state.input_box = ""
        with st.spinner(text='😶‍🌫️ 답변을 생성 중입니다. 잠시만 기다려주세요...', width='content'):
            result = chain.invoke({'topic': user_text})
            st.session_state.messages.append(('ai', result))
            

# -- 입력창과 버튼 생성 --
col1, col2 = st.columns([6, 1], vertical_alignment='bottom')

with col1:
    st.text_input('### LangCahin + Streamlit : 대화형 예제', placeholder='당신이 찾고자 하는 주제를 입력하세요...', key='input_box', on_change=process_input)

with col2:
    st.button('전송', use_container_width=True, on_click=process_input)

# 말풍선
for role, text in st.session_state.messages:
    # st.write(text)
    if role == 'user':
        st.markdown(
                    f"""
                    <div style='text-align: right; margin: 10px;'>
                        <div style='
                            display: inline-block; 
                            background-color: #DCF8C6; 
                            padding: 12px; 
                            border-radius: 15px;
                            max-width: 70%;
                            text-align: left;'>
                            <b style='color: #075E54;'>🥸 사용자</b>
                            <br>{text}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True)
    elif role == 'ai':
        st.markdown(f"""
                    <div style='text-align: left; margin: 10px;'>
                        <div style='
                            display: inline-block; 
                            background-color: #E6E6E6; 
                            padding: 12px; 
                            border-radius: 15px;
                            max-width: 70%;
                            text-align: left;'>
                            <b style='color: #333;'>🤖 AI</b>
                            <br>{text}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True)
                            
    
