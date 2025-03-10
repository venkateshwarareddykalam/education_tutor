import streamlit as st
from PIL import Image
import time

# Import modules
from config import MODEL_NAME, setup_session_state
from utils.text_extraction import extract_text_from_image, extract_text_from_pdf, extract_text_from_docx
from utils.api import get_educational_response, validate_api_key
from utils.cache import clear_cache
from utils.translations import translate, lang_code, LANGUAGES, selected_language
from ui.sidebar import render_sidebar
from ui.components import render_file_upload_section, render_query_section

# Import new modules
from utils.calender import render_calendar_page, render_gamification_dashboard, update_streak

def main():
    """Main application entry point"""
    # Setup page configuration
    st.set_page_config(page_title="Education Tutor", layout="wide")
    
    # Initialize session state
    setup_session_state()
    
    # Update streak on app load
    update_streak()
    
    # Render sidebar
    render_sidebar()
    
    # Determine which page to show based on navigation
    active_page = st.session_state.get("active_page", "main")
    
    if active_page == "main":
        render_main_page()
    elif active_page == "calendar":
        render_calendar_page()
    elif active_page == "gamification":
        render_gamification_dashboard()

def render_main_page():
    """Render the main tutor page"""
    # Main application title
    st.title(translate("app_title"))
    st.write(translate("upload_text"))
    
    # Render file upload section
    render_file_upload_section()
    
    # Combine all extracted text
    combined_text = f"{st.session_state.image_text}\n\n{st.session_state.document_text}".strip()
    
    # Render query section
    st.markdown("---")
    render_query_section(combined_text)
    
    # Disclaimer
    st.markdown("---")
    st.markdown(translate("disclaimer"))

if __name__ == "__main__":
    main()