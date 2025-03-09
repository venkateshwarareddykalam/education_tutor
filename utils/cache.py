import streamlit as st
import os
import json
import hashlib
from datetime import datetime

@st.cache_data(ttl=3600)
def get_cached_response(content_key, lang="en"):
    """Check if we have a cached response for this content in the specified language"""
    cache_file = f"cache_{hashlib.md5(content_key.encode()).hexdigest()}_{lang}.json"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            return cache_data.get('response')
    
    return None

def save_to_cache(content_key, response, lang="en"):
    """Save API response to cache file with language tag"""
    cache_file = f"cache_{hashlib.md5(content_key.encode()).hexdigest()}_{lang}.json"
    cache_data = {
        'response': response,
        'timestamp': datetime.now().isoformat()
    }
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f)

def clear_cache():
    """Clear all cached responses"""
    cache_files = [f for f in os.listdir() if f.startswith("cache_")]
    for file in cache_files:
        os.remove(file)
    st.success("Cache cleared! Next analysis will generate fresh results.")