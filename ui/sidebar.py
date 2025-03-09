import streamlit as st
from datetime import datetime

from config import AVAILABLE_MODELS, MODEL_NAME
from utils.translations import LANGUAGES
from utils.api import validate_api_key
from utils.cache import clear_cache

def render_sidebar():
    """Render the sidebar with all its components"""
    st.sidebar.header("API Configuration")
    
    # API Key input
    groq_api_key = "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"
    
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
    
    # API test button
    #if st.sidebar.button("Test API Connection"):
    #    validate_api_key()
    
    # Usage tracking
    #st.sidebar.markdown("### API Usage Tracker")
    #today = datetime.now().strftime("%Y-%m-%d")
    #usage_key = f"usage_count_{today}"
    #if usage_key not in st.session_state:
    #    st.session_state[usage_key] = 0
    #st.sidebar.text(f"Requests today: {st.session_state[usage_key]}")
    
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

    This application is for educational assistance only.
    """)