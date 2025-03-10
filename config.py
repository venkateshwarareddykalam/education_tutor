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
    
    # Add toggle state for image caption
    if "use_image_caption" not in st.session_state:
        st.session_state.use_image_caption = True
    
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
    
    # User identification
    if "user_id" not in st.session_state:
        st.session_state.user_id = "default_user"  # In a real app, you'd use authentication
    
    # Streak tracking
    if "last_active_date" not in st.session_state:
        st.session_state.last_active_date = None
    if "current_streak" not in st.session_state:
        st.session_state.current_streak = 0
    if "longest_streak" not in st.session_state:
        st.session_state.longest_streak = 0
    
    # Gamification
    if "points" not in st.session_state:
        st.session_state.points = 0
    if "level" not in st.session_state:
        st.session_state.level = 1
    if "achievements" not in st.session_state:
        st.session_state.achievements = []
    
    # Active page tracking
    if "active_page" not in st.session_state:
        st.session_state.active_page = "main"  # Options: main, calendar, gamification