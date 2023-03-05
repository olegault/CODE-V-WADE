# import io
# import csv
# import time
import pandas as pd
import requests
# import pycurl
# import certifi
# import get_top_apps
from google_play_scraper import app
# from policy-scraping import get_policy




r = requests.post(

    "https://api.deepai.org/api/summarization",
    data={
        'text': 'https://helloclue.com/privacy',
    },
    headers={'api-key': '62094660-0461-4c8a-9885-7243213f3b81'}
)
print(r.json())


