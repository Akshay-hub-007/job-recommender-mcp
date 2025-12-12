import filtz
import os
from dotenv import load_dotenv
import google.genai as genai
from apify_client import ApifyClient

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ("GOOGLE_API_KEY")=GOOGLE_API_KEY
client = genai(GOOGLE_API_KEY=GOOGLE_API_KEY)

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))


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


client = genai.Client(api_key=GOOGLE_API_KEY)

def ask_gemini(prompt, max_token=500):

    model = client.generative_models("gemini-2.5-flash")

    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        generation_config={
            "max_output_tokens": max_token,
            "temperature":0.5,
        },
    )

    return response.text


def fetch_linkedin_jobs(search_query,location="india",rows=60):
    run_input = {
        "title" : search_query,
        "location":location,
        "rows":rows,
        "proxy":{
            "useApifyProxy":True,
            "apifyProxyGroups":["RESIDENTIAL"]
        }
    }

    run = client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


def fetch_naukri_jobs(search_query,location="india",rows=60):
    pass

