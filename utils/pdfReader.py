# Import the PdfReader class from pypdf library
from pypdf import PdfReader

def read_pdf(file_path):
    try:
        # Open the PDF file in binary read mode
        with open(file_path, 'rb') as file:
            # Create a PdfReader object
            reader = PdfReader(file)
            # Initialize an empty string to store the text
            text = ""
            # Loop through each page in the PDF
            for page in reader.pages:
                # Extract text from the page and add it to the string
                text += page.extract_text()
            return text
    
    except FileNotFoundError:
        return "Error: The PDF file was not found."
    except Exception as e:
        return f"Error: An issue occurred while reading the PDF - {str(e)}"
