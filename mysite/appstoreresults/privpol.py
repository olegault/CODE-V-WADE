import io
import sys
import StringIO
#import csv
#import time
#import pandas as pd
import requests
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

text = r.txt
arr = []#delte data
if "identifying information" in text:
    arr[0]=1
if "non-reproductive" in text:
    arr[1]=1
if "medication" in text:
    arr[2]=1
if "period calendar" in text:
    arr[3]=1
if "deletion" in text:
    arr[4]=1
if "control" in text:
    arr[5]=1
if "control" and "shared" in text:
    arr[6]=1
#ret arr
print(r.json())


