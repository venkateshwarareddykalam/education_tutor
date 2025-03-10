import streamlit as st
from PIL import Image

from config import SUBJECTS, GRADE_LEVELS, LEARNING_STYLES
from utils.translations import translate, lang_code
from utils.text_extraction import extract_text_from_image, extract_text_from_pdf, extract_text_from_docx
from utils.api import get_educational_response
from utils.imgDis import get_image_info

def render_file_upload_section():
    """Render the file upload section"""
    col1, col2 = st.columns(2)
    
    with col1:
        
        
        uploaded_image = st.file_uploader(
            translate("upload_img_button"), 
            type=["jpg", "png", "jpeg"]
        )
        # Add caption toggle option
        use_caption = st.checkbox("Image Have Other than text info ", value=True, help="Enabling this will tell our system that there is data other than text Ex:- Diagram,objects..etc")
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            with st.spinner("Extracting data from image..."):
                # Extract text with OCR
                extracted_text = extract_text_from_image(image)
                
                # If caption is enabled, get image description
                if use_caption:
                    with st.spinner("Extracting Intel info from image"):
                        try:
                            image_caption = get_image_info(image)
                            #st.success(f"Generated caption: {image_caption}")
                            # Combine OCR text with caption
                            st.session_state.image_text = f"Image Info: {image_caption}\n\nExtracted Text: {extracted_text}"
                        except Exception as e:
                            st.error(f"Error generating caption: {str(e)}")
                            st.session_state.image_text = extracted_text
                else:
                    # Skip caption generation
                    st.session_state.image_text = extracted_text
                
                #st.write("**Text extracted from image:**")
                #st.write(st.session_state.image_text)
    
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
                
                #st.write("**Text extracted from document:**")
                #st.write(st.session_state.document_text)

def render_query_section(combined_text):
    """Render the query section with chat functionality"""
    st.subheader(translate("questions_header"))
    
    # Subject selection
    selected_subject = st.selectbox("Select Subject", SUBJECTS)
    
    # Grade level selection
    selected_grade = st.selectbox("Education Level", GRADE_LEVELS)
    
    # Learning style preference
    selected_style = st.selectbox("Preferred Learning Style", LEARNING_STYLES)
    
    # Chat title input for current chat
    current_chat_id = st.session_state.current_chat_id
    if current_chat_id not in st.session_state.chat_titles:
        st.session_state.chat_titles[current_chat_id] = translate("new_chat_default")
    
    # Allow user to change chat title
    chat_title = st.text_input(
        translate("chat_title"), 
        value=st.session_state.chat_titles[current_chat_id],
        key=f"title_{current_chat_id}"
    )
    st.session_state.chat_titles[current_chat_id] = chat_title
    
    # Initialize chat history for this chat if it doesn't exist
    if current_chat_id not in st.session_state.chat_history:
        st.session_state.chat_history[current_chat_id] = []
    
    # Display chat history for current chat with improved styling
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history[current_chat_id]:
            st.markdown("### Chat Conversation")
            for msg in st.session_state.chat_history[current_chat_id]:
                if msg["role"] == "user":
                    st.markdown(
                        f"""<div style="background-color: #070708; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                        <strong>You:</strong> {msg['content']}
                        </div>""", 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""<div style="background-color: #1a5950; padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #039be5;">
                        <strong>Tutor:</strong> {msg['content']}
                        </div>""", 
                        unsafe_allow_html=True
                    )
    
    # User query
    user_query = st.text_area(translate("question_input"), height=100)
    
    if st.button(translate("ask_button")) and user_query:
        # Save user message to chat history
        st.session_state.chat_history[current_chat_id].append({
            "role": "user", 
            "content": user_query
        })
        
        # Get context from previous exchanges
        chat_context = ""
        if len(st.session_state.chat_history[current_chat_id]) > 1:
            # Extract last few exchanges for context
            last_exchanges = st.session_state.chat_history[current_chat_id][-4:] if len(st.session_state.chat_history[current_chat_id]) > 4 else st.session_state.chat_history[current_chat_id]
            chat_context = "\n".join([f"{'User' if msg['role'] == 'user' else 'Tutor'}: {msg['content']}" for msg in last_exchanges[:-1]])
        
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
                    lang_code,
                    chat_context  # Pass chat context for follow-up questions
                )
                
                # Add response to chat history
                st.session_state.chat_history[current_chat_id].append({
                    "role": "assistant", 
                    "content": response
                })
                
                # Refresh the page to show updated chat
                st.rerun()