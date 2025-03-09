import streamlit as st

# Language options
LANGUAGES = {
    "English": "en",
    "हिन्दी (Hindi)": "hi", 
    "বাংলা (Bengali)": "bn",
    "తెలుగు (Telugu)": "te",
    "मराठी (Marathi)": "mr",
    "தமிழ் (Tamil)": "ta",
    "ગુજરાતી (Gujarati)": "gu",
    "ಕನ್ನಡ (Kannada)": "kn",
    "മലയാളം (Malayalam)": "ml",
    "ਪੰਜਾਬੀ (Punjabi)": "pa",
    "ଓଡ଼ିଆ (Odia)": "or",
    "অসমীয়া (Assamese)": "as",
}

# Translations dictionary
TRANSLATIONS = {
    # Add to the TRANSLATIONS dictionary in utils/translations.py
# Add these entries to the "en" dictionary
"en": {
    "app_title": "📚 Education Tutor",
    "upload_text": "Upload study materials or ask questions to get personalized tutoring.",
    "upload_img_button": "Upload Image",
    "upload_doc_button": "Upload Document (PDF, DOCX)",
    "analyze_button": "Analyze Content",
    "ask_button": "Ask Question",
    "loading_text": "Processing your content...",
    "results_header": "Analysis Results:",
    "combined_input": "Combined Input:",
    "questions_header": "Educational Question Assistant",
    "question_input": "Ask any educational question:",
    "disclaimer": "⚠️ Note: This educational tool is designed to assist learning. Always verify information with trusted educational resources.",
    # New translation keys
    "chat_history": "Chat History",
    "new_chat": "New Chat",
    "saved_chats": "Previous Chats",
    "new_chat_default": "New Conversation",
    "chat_title": "Chat Title"
},

# Add these entries to the "hi" dictionary
"hi": {
    # Existing entries
    "app_title": "📚 शिक्षा ट्यूटर",
    "upload_text": "व्यक्तिगत ट्यूटरिंग प्राप्त करने के लिए अध्ययन सामग्री अपलोड करें या प्रश्न पूछें।",
    "upload_img_button": "छवि अपलोड करें",
    "upload_doc_button": "दस्तावेज़ अपलोड करें (पीडीएफ, डीओसीएक्स)",
    "analyze_button": "सामग्री का विश्लेषण करें",
    "ask_button": "प्रश्न पूछें",
    "loading_text": "आपकी सामग्री संसाधित की जा रही है...",
    "results_header": "विश्लेषण परिणाम:",
    "combined_input": "संयुक्त इनपुट:",
    "questions_header": "शैक्षिक प्रश्न सहायक",
    "question_input": "कोई भी शैक्षिक प्रश्न पूछें:",
    "disclaimer": "⚠️ नोट: यह शैक्षिक उपकरण सीखने में सहायता के लिए डिज़ाइन किया गया है। हमेशा विश्वसनीय शैक्षिक संसाधनों के साथ जानकारी सत्यापित करें।",
    # New translation keys
    "chat_history": "चैट इतिहास",
    "new_chat": "नई चैट",
    "saved_chats": "पिछली चैट",
    "new_chat_default": "नई बातचीत",
    "chat_title": "चैट शीर्षक"
},
    # Add other language translations as needed
}

# Get the selected language
def get_selected_language():
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "English"
    return st.session_state.selected_language

selected_language = get_selected_language()
lang_code = LANGUAGES[selected_language]

def translate(key):
    """Translate a key to the selected language"""
    if lang_code in TRANSLATIONS and key in TRANSLATIONS[lang_code]:
        return TRANSLATIONS[lang_code][key]
    return TRANSLATIONS["en"][key]