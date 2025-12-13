from dotenv import load_dotenv
from apify_client import ApifyClient
import os
load_dotenv()


apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

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
    run_input = {
        "keyword" : search_query,
        "maxJobs" : 60,
        "freshness" : "all",
        "sortby" : "relevance",
        "experience" :" all"
    }

    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

