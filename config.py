import streamlit as st
from datetime import datetime

# Model settings
MODEL_NAME = "llama3-70b-8192"
AVAILABLE_MODELS = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]

# Subject options
SUBJECTS = ["General", "Mathematics", "Science", "History", "Language Arts", 
            "Computer Science", "Geography", "Economics", "Physics", "Chemistry", 
            "Biology", "Literature", "Philosophy"]

# Grade level options
GRADE_LEVELS = ["Elementary School", "Middle School", "High School", "College/University", "Professional"]

# Learning style options
LEARNING_STYLES = ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "No Preference"]

# API settings
MAX_RETRIES = 3
RETRY_DELAY = 2
MAX_TOKENS = 2048
TEMPERATURE = 0.4

def setup_session_state():
    """Initialize session state variables"""
    if "image_text" not in st.session_state:
        st.session_state.image_text = ""
    
    if "document_text" not in st.session_state:
        st.session_state.document_text = ""
        
    # Usage tracking
    today = datetime.now().strftime("%Y-%m-%d")
    usage_key = f"usage_count_{today}"
    if usage_key not in st.session_state:
        st.session_state[usage_key] = 0
# Add to config.py
def setup_session_state():
    """Initialize session state variables"""
    if "image_text" not in st.session_state:
        st.session_state.image_text = ""
    
    if "document_text" not in st.session_state:
        st.session_state.document_text = ""
    
    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}  # Dictionary to store chats by ID
    
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    if "chat_titles" not in st.session_state:
        st.session_state.chat_titles = {}  # Store chat titles for sidebar
        
    # Usage tracking
    today = datetime.now().strftime("%Y-%m-%d")
    usage_key = f"usage_count_{today}"
    if usage_key not in st.session_state:
        st.session_state[usage_key] = 0