import streamlit as st
from chatbot_core import Chatbot

st.set_page_config(page_title="Chatbot", layout="centered")

if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()

if "history" not in st.session_state:
    st.session_state.history = []

bot = st.session_state.bot

st.sidebar.title("Settings")
name_in = st.sidebar.text_input("Bot name", value=bot.bot_name)
primary = st.sidebar.color_picker("Primary color", value=bot.theme.get("primary_color", "#0b5cff"))
background = st.sidebar.color_picker("Background color", value=bot.theme.get("background", "#ffffff"))
avatar = st.sidebar.file_uploader("Upload avatar (optional)", type=["png", "jpg", "jpeg"])

if st.sidebar.button("Apply"):
    bot.set_name(name_in.strip() or bot.bot_name)
    bot.set_theme(primary_color=primary, background=background)
    st.experimental_rerun()

# Inject simple CSS for theme/background
css = f"""
<style>
    .stApp {{
        background: {bot.theme.get("background", "#ffffff")};
    }}
    .chat-bot {{
        border-radius: 12px;
        padding: 8px 12px;
        margin: 6px 0;
        background-color: {bot.theme.get("primary_color", "#0b5cff")};
        color: white;
    }}
    .chat-user {{
        border-radius: 12px;
        padding: 8px 12px;
        margin: 6px 0;
        background-color: #f1f1f1;
    }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title(bot.bot_name)
if avatar:
    st.image(avatar, width=80)

with st.form("msg_form", clear_on_submit=True):
    user_input = st.text_input("You", "")
    pressed = st.form_submit_button("Send")
if pressed and user_input:
    resp, _ = bot.get_response(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append((bot.bot_name, resp))

# Display history (most recent at bottom)
for speaker, text in st.session_state.history:
    if speaker == "You":
        st.markdown(f"<div class='chat-user'><strong>You:</strong> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bot'><strong>{speaker}:</strong> {text}</div>", unsafe_allow_html=True)

st.sidebar.markdown("### Quick Commands")
st.sidebar.markdown("- `/help` — list commands")
st.sidebar.markdown("- `/name` — bot name")
st.sidebar.markdown("- `/setname YourName`")
st.sidebar.markdown("- `/time`, `/date`, `/joke`")
st.sidebar.markdown("- `/calc 2+2*3`")
st.sidebar.markdown("- `/open https://example.com`")

st.write("🔹 Try commands: `/weather Delhi`, `/news sports`, `/news ai`")

