import streamlit as st
from streamlit_chat import message

#side bar
if "api_key" not in st.session_state:
    st.session_state['api_key'] = False

sidebar = st.sidebar

sidebar.header("Chatbot")
sidebar.text("copilot")
#st.session_state['api_key'] = True
if not st.session_state['api_key']:
    sidebar.error(":x: API 인증 안됨")
else :
    sidebar.success(":white_check_mark: API 인증 완료")

sidebar.subheader("Models and parameters")

model = sidebar.selectbox(
    label="모델 선택",
    options=["모델1", "모델2", "모델3"]
)

temperature = sidebar.slider(
    label="temperature",
    min_value=0.01,
    max_value=5.00,
    step=0.01
)

top_p = sidebar.slider(
    label="top_p",
    min_value=0.01,
    max_value=1.00,
    step=0.01,
    value=0.90
)

max_length = sidebar.slider(
    label= "max_length",
    min_value=32,
    max_value=128,
    step = 1,
    value=120
)

sidebar.button(
    label= "Clear Chat History"
)  

#chat
class chat:
    msg: str = None
    sender: str = None

if 'chat' not in st.session_state:
    st.session_state['chat'] = []

prompt = st.chat_input()
if prompt:
    chatting = chat()
    chatting.msg = prompt
    chatting.sender = 'user'
    st.session_state.chat.append(chatting)


#채팅 출력
for i in st.session_state['chat']: 
    with st.chat_message(i.sender):
        st.write(i.msg)