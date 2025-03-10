import streamlit as st
from datetime import datetime

from config import AVAILABLE_MODELS, MODEL_NAME
from utils.translations import LANGUAGES, translate
from utils.api import validate_api_key
from utils.cache import clear_cache
from dotenv import load_dotenv
import os

load_dotenv()

def render_sidebar():
    """Render the sidebar with all its components"""
    # Navigation menu
    st.sidebar.title("Navigation")
    
    # Navigation buttons
    main_nav = st.sidebar.button("📚 Main Tutor", use_container_width=True)
    calendar_nav = st.sidebar.button("📅 Learning Calendar", use_container_width=True)
    gamification_nav = st.sidebar.button("🏆 Progress & Achievements", use_container_width=True)
    
    # Handle navigation
    if main_nav:
        st.session_state.active_page = "main"
    if calendar_nav:
        st.session_state.active_page = "calendar"
    if gamification_nav:
        st.session_state.active_page = "gamification"
    
    st.sidebar.markdown("---")
    
    # Display streak and points
    st.sidebar.subheader("Your Progress")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("🔥 Streak", st.session_state.get("current_streak", 0))
    with col2:
        st.metric("⭐ Points", st.session_state.get("points", 0))
    
    st.sidebar.markdown("---")
    
    # Chat History Section
    st.sidebar.header(translate("chat_history"))
    
    # New Chat Button
    if st.sidebar.button(translate("new_chat")):
        # Generate a new chat ID
        new_chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
        # Reset the current chat messages
        st.session_state.chat_history[new_chat_id] = []
        # Set default title
        st.session_state.chat_titles[new_chat_id] = translate("new_chat_default")
        # Update current chat ID
        st.session_state.current_chat_id = new_chat_id
    
    # Display saved chats
    if st.session_state.chat_titles:
        st.sidebar.subheader(translate("saved_chats"))
        for chat_id, title in st.session_state.chat_titles.items():
            # Use the actual stored title instead of the default
            display_title = title if title != "" else "Unnamed Convo"
            if st.sidebar.button(f"{display_title}", key=f"chat_{chat_id}"):
                st.session_state.current_chat_id = chat_id
    
    st.sidebar.markdown("---")
    
    # Original sidebar content
    st.sidebar.header("API Configuration")
    
    # API Key input
    groq_api_key = os.getenv("GROQ_URL")
    st.session_state["groq_api_key"] = groq_api_key
    # Language settings
    st.sidebar.header("Language Settings")
    selected_language = st.sidebar.selectbox(
        "Select Language", 
        options=list(LANGUAGES.keys()),
        index=