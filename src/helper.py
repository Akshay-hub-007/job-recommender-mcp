import filtz
import os
from dotenv import load_dotenv

def extract_text_from_pdf(uploaded_file):
    """
    Docstring for extract_text_from_pdf
    
    :param pdf_path: Description
    """
    doc = filtz.open(stream=uploaded_file.read(),file_type="pdf")
    
    text = ""
    for page in doc:
        text += page.get_text()
    return text