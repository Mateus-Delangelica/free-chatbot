from dataclasses import dataclass
from typing import Literal
import streamlit as st
import traceback
from gradio_client import Client
import base64

try:
    client = Client("yuntian-deng/ChatGPT4")

except ValueError as e:
    error_message = f"Erro ao obter informações da API: {e}"
    error_traceback = traceback.format_exc()
    st.error(f"{error_message}\nDetalhes do erro:\n{error_traceback}")
    client = None

@dataclass
class Message:
    origin: Literal["humano", "chatbot"] 
    message: str

# ----- Functions -----
def initialize_session_state():
    if "history" not in st.session_state: 
        st.session_state.history = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = client

def on_click_callback():
    human_prompt = st.session_state.human_prompt
    try:
        api_response = st.session_state.conversation.predict(
            inputs=human_prompt,
            temperature=0.6,
            top_p=0.9,
            api_name="/predict"
        )
        response = api_response[0][-1][-1]

    except Exception as e:
        response = f"Erro ao tentar gerar a resposta: {str(e)}"
        
    st.session_state.history.append(
        Message("humano", human_prompt)
    )
    st.session_state.history.append(
        Message("chatbot", response)
    )
    st.session_state.human_prompt = ""

def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# ----- -------- -----
load_css()
initialize_session_state()

# st.image("static/XP5.png", width=200)
st.image("static/tucano.png", width=200)
st.title("Faça uma pergunta")

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
teste_placeholder = st.empty()

with chat_placeholder:
    for chat in st.session_state.history:
        def get_base64_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')

        # bot_image_base64 = get_base64_image("static/option01bot.png")
        # bot_image_base64 = get_base64_image("static/Option_02_Xp_Bot.png")
        bot_image_base64 = get_base64_image("static/Option_05_Xp_Bot.png")

        # user_image_base64 = get_base64_image("static/option01user.png")
        user_image_base64 = get_base64_image("static/Option_02_Xp_User.png")
        # user_image_base64 = get_base64_image("Option_03_Xp_User.png")

        div = f"""
        <div class="chat-row {'row-reverse' if chat.origin == "humano" else ''}">
            <img src="data:image/png;base64,{
            bot_image_base64 if chat.origin == "chatbot" 
            else user_image_base64
            }" width=50 height=50 style="margin: 10px;">
            <div class="{'human-text-bubble' if chat.origin == "humano" else 'chatbot-text-bubble'}">{chat.message}</div>
        </div>
        """
        st.markdown(div, unsafe_allow_html=True)
        for _ in range(2):
            st.markdown("")

with prompt_placeholder:
    cols = st.columns([6, 1])
    with cols[0]:
        st.text_input(
            "Chat", 
            value="", 
            key="human_prompt"
        )
    with cols[1]:
        with st.container():
            st.markdown('<div class="submit-button">', unsafe_allow_html=True)
            st.form_submit_button(
                "Enviar",
                on_click=on_click_callback
            )
            st.markdown('</div>', unsafe_allow_html=True)