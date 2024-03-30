import streamlit as st
from st_multimodal_chatinput import multimodal_chatinput
import openai

client = openai

#응답 요청 함수
def get_completion(prompt, model, temperature):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

if "api_key" not in st.session_state:
    st.session_state['api_key'] = None
    
#side bar
sidebar = st.sidebar

sidebar.header("Chatbot")
sidebar.text("copilot")

with sidebar.form("API Key 입력"):
    key = st.text_input("API Key 입력")
    submitted = st.form_submit_button("확인")
    if submitted:
        st.session_state['api_key'] = key
        client.api_key = st.session_state['api_key']
        
#st.session_state['api_key'] = True
if not st.session_state['api_key']:
    sidebar.error(":x: API 인증 안됨")
else :
    sidebar.success(":white_check_mark: API 인증 완료")

sidebar.subheader("Models and parameters")

model = sidebar.selectbox(
    label="모델 선택",
    options=["gpt-3.5-turbo", "모델2", "모델3"]
)

#temperature
temperature = sidebar.slider(
    label="temperature",
    min_value=0.01,
    max_value=5.00,
    step=0.01
)

#top_p
top_p = sidebar.slider(
    label="top_p",
    min_value=0.01,
    max_value=1.00,
    step=0.01,
    value=0.90
)

#max_length
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
    img = None
    msg: str = None
    sender: str = None

if 'chat' not in st.session_state:
    st.session_state['chat'] = []


#채팅 출력
# for i in st.session_state['chat']: 
#     with st.chat_message(i.sender):
#         st.write(i.msg)

chatContainer = st.container(height=450)
userInput = multimodal_chatinput()

for i in st.session_state['chat']:
    with chatContainer:
        with st.chat_message(i.sender):
            if i.img:
                st.image(i.img)
            st.write(i.msg)

if userInput :
    #유저 입력
    chatting = chat()
    if userInput['images']:
        chatting.img = userInput['images']
    chatting.msg = userInput['text']
    chatting.sender = 'user'
    st.session_state['chat'].append(chatting)
    #메시지 출력
    with chatContainer:
        with st.chat_message('user'):
            if userInput['images']:
                st.image(userInput['images'])
            st.write(userInput['text'])
        # for i in st.session_state['chat']:
        #     with st.chat_message(i.sender):
        #         if i.img:
        #             st.image(i.img)
        #         st.write(i.msg)
    #챗봇
    response_message = get_completion(userInput['text'], model, temperature)
    response = chat()
    response.msg = response_message
    response.sender = 'ai'
    st.session_state['chat'].append(response)
    #메시지 출력
    with chatContainer:
        with st.chat_message('ai'):
            st.write(response_message)
    # with chatContainer:
    #     for i in st.session_state['chat']:
    #         if i.sender is 'ai':
    #             with st.chat_message(i.sender):
    #                st.write(i.msg)