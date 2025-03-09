import streamlit as st
import numpy as np
import cv2
from PIL import Image
import PyPDF2
#import docx
import easyocr
from utils.pdfReader import read_pdf  # Import the read_pdf function

# Initialize OCR reader (globally to avoid reinitialization)
@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['en'])

def extract_text_from_image(image):
    """Extract text from image using OCR"""
    try:
        # Get OCR reader
        reader = get_ocr_reader()
        
        # Convert PIL Image to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Perform OCR
        result = reader.readtext(image_cv)
        extracted_text = "\n".join([text[1] for text in result])
        
        return extracted_text
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF document using the improved pdfReader function"""
    try:
        # Create a temporary file to use with read_pdf function
        with open("temp_pdf.pdf", "wb") as f:
            f.write(pdf_file.getvalue())
        
        # Use the read_pdf function from pdfReader.py
        extracted_text = read_pdf("temp_pdf.pdf")
        
        # Clean up the temporary file
        import os
        os.remove("temp_pdf.pdf")
        
        return extracted_text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def extract_text_from_docx(docx_file):
    return "no data indoc "