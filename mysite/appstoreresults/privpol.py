import io
#import csv
#import time
#import pandas as pd
#import requests
import get_top_apps
from google_play_scraper import app
#from policy-scraping import get_policy


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
    headers={'api-key': '62094660-0461-4c8a-9885-7243213f3b81'}
)
print(r.json())


