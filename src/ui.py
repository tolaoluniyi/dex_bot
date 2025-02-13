import streamlit as st
import yaml
from src.bot import DexBot
from src.utils import load_config, log_message

# Page configuration
st.set_page_config(page_title="Dex Bot UI", layout="wide")

# Custom CSS
def load_css():
    with open("ui/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Sidebar for configuration
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Bitget API Key")
api_secret = st.sidebar.text_input("Bitget API Secret", type="password")
api_passphrase = st.sidebar.text_input("Bitget API Passphrase", type="password")
telegram_token = st.sidebar.text_input("Telegram Bot Token")
telegram_chat_id = st.sidebar.text_input("Telegram Chat ID")

if st.sidebar.button("Save Configuration"):
    config = {
        "bitget": {
            "api_key": api_key,
            "api_secret": api_secret,
            "api_passphrase": api_passphrase,
        },
        "telegram": {
            "bot_token": telegram_token,
            "chat_id": telegram_chat_id,
        },
    }
    with open("config/config.yaml", "w") as f:
        yaml.dump(config, f)
    st.sidebar.success("Configuration saved!")

# Main dashboard
st.title("Dex Bot Dashboard")

# Start/Stop bot
if st.button("Start Bot"):
    bot = DexBot()
    bot.run()
    st.success("Bot started!")

if st.button("Stop Bot"):
    st.warning("Bot stopped!")

# Display logs
st.subheader("Logs")
with open("data/logs/bot.log", "r") as f:
    logs = f.read()
st.text_area("Log Output", logs, height=300)

# Display token data
st.subheader("Token Data")
token_data = load_config("data/coins/tokens.json")
st.write(token_data)
