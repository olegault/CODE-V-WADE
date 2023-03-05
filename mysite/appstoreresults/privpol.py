import io
import csv
import time
import pandas as pd
import requests
import pycurl
import certifi
import get_top_apps
from google_play_scraper import app
from policy-scraping import get_policy



r = requests.post(

    "https://api.deepai.org/api/summarization",
    data={
        'text': 'YOUR_TEXT_URL',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


