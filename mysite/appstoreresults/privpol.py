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


link = input("Enter Play Store Link: ")
package = link.split('id=')[1].split('&')[0]
result = app(
    package,
    lang='en', # defaults to 'en'
    country='us' # defaults to 'us'
)
policy_link = result['privacyPolicy']

r = requests.post(

    "https://api.deepai.org/api/summarization",
    data={
        'text': policy_link,
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


