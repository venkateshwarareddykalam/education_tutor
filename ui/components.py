import streamlit as st
from PIL import Image

from config import SUBJECTS, GRADE_LEVELS, LEARNING_STYLES
from utils.translations import translate, lang_code
from utils.text_extraction import extract_text_from_image, extract_text_from_pdf, extract_text_from_docx
from utils.api import get_educational_response

def render_file_upload_section():
    """Render the file upload section"""
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_image = st.file_uploader(
            translate("upload_img_button"), 
            type=["jpg", "png", "jpeg"]
        )
        
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            with st.spinner("Extracting text from image..."):
                st.session_state.image_text = extract_text_from_image(image)
                st.write("**Text extracted from image:**")
                st.write(st.session_state.image_text)
    
    with col2:
        uploaded_document = st.file_uploader(
            translate("upload_doc_button"), 
            type=["pdf", "docx"]
        )
        
        if uploaded_document is not None:
            with st.spinner("Extracting text from document..."):
                if uploaded_document.name.endswith('.pdf'):
                    st.session_state.document_text = extract_text_from_pdf(uploaded_document)
                elif uploaded_document.name.endswith('.docx'):
                    st.session_state.document_text = extract_text_from_docx(uploaded_document)
                
                st.write("**Text extracted from document:**")
                st.write(st.session_state.document_text)

def render_query_section(combined_text):
    """Render the query section"""
    st.subheader(translate("questions_header"))
    
    # Subject selection
    selected_subject = st.selectbox("Select Subject", SUBJECTS)
    
    # Grade level selection
    selected_grade = st.selectbox("Education Level", GRADE_LEVELS)
    
    # Learning style preference
    selected_style = st.selectbox("Preferred Learning Style", LEARNING_STYLES)
    
    # User query
    user_query = st.text_area(translate("question_input"), height=100)
    
    if st.button(translate("ask_button")) and user_query:
        # Display combined input for reference
        if combined_text:
            st.write(translate("combined_input"))
            with st.expander("Show Combined Input"):
                st.write(combined_text)
        
        with st.spinner(translate("loading_text")):
            if not st.session_state.get("groq_api_key"):
                st.warning("Please enter a Groq API key in the sidebar to use this feature.")
            else:
                response = get_educational_response(
                    combined_text, 
                    user_query, 
                    selected_subject, 
                    selected_grade, 
                    selected_style,
                    lang_code
                )
                st.markdown("### Response:")
                st.markdown(response)