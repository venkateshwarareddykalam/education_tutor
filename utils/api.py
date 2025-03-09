import streamlit as st
import requests
import time
import random
from datetime import datetime

from config import MODEL_NAME, MAX_RETRIES, RETRY_DELAY, TEMPERATURE, MAX_TOKENS
from utils.cache import get_cached_response, save_to_cache
from utils.translations import selected_language

def validate_api_key():
    """Validate the Groq API key"""
    groq_api_key = st.session_state.get("groq_api_key", "")
    
    if not groq_api_key:
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        test_payload = {
            "messages": [{"role": "user", "content": "Hello"}],
            "model": MODEL_NAME
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                                json=test_payload, 
                                headers=headers)
        if response.status_code == 200:
            st.sidebar.success("✅ Groq API key is valid")
            return True
        else:
            st.sidebar.error(f"❌ API key error: {response.status_code}")
            return False
    except Exception as e:
        st.sidebar.error(f"❌ API key error: {str(e)}")
        return False

def exponential_backoff(retries, max_retries=MAX_RETRIES, initial_delay=RETRY_DELAY):
    """Calculate delay with exponential backoff and jitter"""
    if retries >= max_retries:
        return None  
    delay = initial_delay * (2 ** retries) + (random.random() * 0.5)  
    return min(delay, 60)
# Modify get_educational_response in utils/api.py
def get_educational_response(combined_text, user_query, subject="General", grade_level="High School", learning_style="Visual", lang_code="en", chat_context=""):
    """Get educational response from Groq API based on combined text and user query with chat context"""
    groq_api_key = st.session_state.get("groq_api_key", "")
    
    if not groq_api_key:
        return "Please enter a Groq API key in the sidebar to get educational insights."
    
    # Generate a unique cache key
    content_key = f"{combined_text}_{user_query}_{subject}_{grade_level}_{learning_style}_{chat_context}"
    
    # Check cache first
    cached_response = get_cached_response(content_key, lang_code)
    if cached_response:
        return f"{cached_response}\n\n(This response was retrieved from cache)"
    
    # Make API request with retries
    for attempt in range(MAX_RETRIES):
        try:
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            
            # Create prompt based on available content, query, and chat context
            prompt = f"""
            You are an educational tutor specializing in {subject}. 
            The student is at a {grade_level} level and prefers {learning_style} learning approaches.
            
            STUDY MATERIAL TEXT:
            {combined_text}
            
            {'PREVIOUS CONVERSATION CONTEXT:' + chat_context if chat_context else ''}
            
            STUDENT QUESTION:
            {user_query}
            
            Based on both the study material and the question, provide a comprehensive educational response that:
            1. Directly answers the student's question
            2. References relevant information from the study material
            3. Explains key concepts clearly and thoroughly
            4. Provides examples or analogies appropriate for their learning style
            5. Suggests additional study approaches for this topic
            {'6. Keep in mind the previous conversation context when answering follow-up questions' if chat_context else ''}
            
            Provide your response in {selected_language} language.
            """
            
            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": f"You are a helpful educational tutor. Respond in {selected_language} language."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API error: {response.status_code} - {response.text}")
            
            # Save successful response to cache
            save_to_cache(content_key, result, lang_code)
            
            # Update usage tracking
            today = datetime.now().strftime("%Y-%m-%d")
            usage_key = f"usage_count_{today}"
            if usage_key not in st.session_state:
                st.session_state[usage_key] = 0
            st.session_state[usage_key] += 1
            
            return result
        
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "rate limit" in error_message.lower():
                backoff_time = exponential_backoff(attempt)
                if backoff_time is not None:
                    time.sleep(backoff_time)
                    continue
                else:
                    return "Rate Limit Exceeded. The API service is currently experiencing high demand. Please try again in a few minutes."
            else:
                return f"Error getting insights: {error_message}"