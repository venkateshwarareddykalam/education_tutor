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
    # Complete the unfinished line for language selection
    selected_language = st.sidebar.selectbox(
        "Select Language", 
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index("English")  # Default to English
    )
    
    # Set language in session state
    st.session_state["language"] = selected_language
    
    # Enhanced gamification section
    st.sidebar.markdown("---")
    st.sidebar.header("🎮 Your Learning Journey")
    
    # Display user level with progress bar
    user_level = st.session_state.get("level", 1)
    level_title = st.session_state.get("level_title", "Beginner Learner")
    
    st.sidebar.subheader(f"Level {user_level}: {level_title}")
    
    # Calculate progress to next level
    current_level_points = st.session_state.get("current_level_points", 0)
    next_level_points = st.session_state.get("next_level_points", 100)
    current_points = st.session_state.get("points", 0)
    
    # Calculate progress percentage
    if next_level_points > current_level_points:
        progress_percentage = (current_points - current_level_points) / (next_level_points - current_level_points)
        progress_percentage = max(0, min(1.0, progress_percentage))  # Constrain between 0 and 1
    else:
        progress_percentage = 1.0
    
    # Display progress bar
    st.sidebar.progress(progress_percentage)
    st.sidebar.caption(f"{current_points} / {next_level_points} points to next level")
    
    # Display badges/achievements
    recent_achievements = st.session_state.get("recent_achievements", [])
    if recent_achievements:
        st.sidebar.subheader("🏆 Recent Achievements")
        for achievement in recent_achievements[:3]:  # Show only the 3 most recent
            st.sidebar.markdown(f"**{achievement['icon']} {achievement['name']}** - {achievement['description']}")
    
    # Daily challenge
    st.sidebar.subheader("🎯 Daily Challenge")
    daily_challenge = st.session_state.get("daily_challenge", {
        "title": "Knowledge Explorer",
        "description": "Ask questions in 3 different subjects today",
        "reward": 25,
        "progress": 0,
        "target": 3
    })
    
    # Display challenge
    st.sidebar.markdown(f"**{daily_challenge['title']}**")
    st.sidebar.caption(f"{daily_challenge['description']}")
    st.sidebar.progress(daily_challenge['progress'] / daily_challenge['target'])
    st.sidebar.caption(f"Progress: {daily_challenge['progress']}/{daily_challenge['target']} • Reward: {daily_challenge['reward']} points")
    
    # Model selection
    st.sidebar.markdown("---")
    st.sidebar.header("Model Settings")
    selected_model = st.sidebar.selectbox(
        "AI Model", 
        options=AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(MODEL_NAME)
    )
    
    # Cache settings
    st.sidebar.header("Cache Settings")
    if st.sidebar.button("Clear Cache"):
        clear_cache()
        st.sidebar.success("Cache cleared successfully!")
    
    # App info
    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        **Educational Tutor App**
        
        Upload learning materials and get AI-assisted tutoring 
        in a variety of subjects and learning styles.
        
        Version: 1.0.0
        """
    )
    