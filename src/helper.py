import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from google import genai
from apify_client import ApifyClient

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

if not APIFY_API_TOKEN:
    raise ValueError("❌ APIFY_API_TOKEN not found in .env")

# Initialize Gemini client
client = genai.Client(api_key=GOOGLE_API_KEY)

# Initialize Apify client
apify_client = ApifyClient(APIFY_API_TOKEN)


def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file"""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()

    return text

def ask_gemini(prompt, max_tokens=500):
    """Send prompt to Gemini and return response text"""

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "max_output_tokens": max_tokens,
        "temperature": 0.5,
    },
)

    return response.text
