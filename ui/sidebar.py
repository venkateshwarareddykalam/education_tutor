# Modify ui/sidebar.py
import streamlit as st
from datetime import datetime

from config import AVAILABLE_MODELS, MODEL_NAME
from utils.translations import LANGUAGES, translate
from utils.api import validate_api_key
from utils.cache import clear_cache

def render_sidebar():
    """Render the sidebar with all its components"""
    # Chat History Section
    st.sidebar.header(translate("chat_history"))
    
    # New Chat Button
    if st.sidebar.button(translate("new_chat")):
        # Generate a new chat ID
        st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
        # Reset the current chat messages
        st.session_state.chat_history[st.session_state.current_chat_id] = []
        # Set default title
        st.session_state.chat_titles[st.session_state.current_chat_id] = translate("new_chat_default")
    
    # Display saved chats
    if st.session_state.chat_titles:
        st.sidebar.subheader(translate("saved_chats"))
        for chat_id, title in st.session_state.chat_titles.items():
            if st.sidebar.button(f"{title}", key=f"chat_{chat_id}"):
                st.session_state.current_chat_id = chat_id
    
    st.sidebar.markdown("---")
    
    # Original sidebar content
    st.sidebar.header("API Configuration")
    
    # API Key input
    groq_api_key = "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"
    st.session_state["groq_api_key"] = groq_api_key
    # Language settings
    st.sidebar.header("Language Settings")
    selected_language = st.sidebar.selectbox(
        "Select Language", 
        options=list(LANGUAGES.keys()),
        index=0,
        key="selected_language"
    )
    
    # Cache management
    if st.sidebar.button("Clear Analysis Cache"):
        clear_cache()
    
    # Model selection
    st.sidebar.markdown("### Model Settings")
    model_option = st.sidebar.selectbox(
        "Select LLM Model",
        AVAILABLE_MODELS,
        index=0,
        key="model_name"
    )
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About This App")
    st.sidebar.markdown("""
    This education tutor app provides:
    1. Analysis of educational content and study materials
    2. AI-powered explanations tailored to your learning style
    3. Support for multiple subjects and education levels
    4. Multi-language support for diverse learners
    5. Response caching to minimize API calls
    6. Chat history for follow-up questions

    This application is for educational assistance only.
    """)