from readabilipy import simple_json_from_html_string
from urllib.parse import quote, unquote
import utilities
from database import Database#read scrape
import requests
#basic readability lib from npm for js
html_string = requests.get("https://enduco.app/en/privacy-policy-app/")

html_string = utilities.get_raw_html(128)

print(html_string)



article = simple_json_from_html_string(html_string, use_readability=True)

plain_text = ''

for element in article['plain_text']:
    plain_text += element['text'] + '\n'

with open("cleaned.html", "w", encoding="utf-8", errors="ignore") as fp:
    fp.write(plain_text)



unquoted_article = unquote(quoted_article, encoding='utf-8', errors='replace')
with open("cleaned-unquote.html", "w", encoding="utf-8", errors="ignore") as fp:
    fp.write(unquoted_article)

with open("plaincleaned.html", "w", encoding="utf-8", errors="ignore") as fp:
    fp.write(article['plain_content'])


with open("plaintext.txt", "w", encoding="utf-8", errors="ignore") as fp:
    for element in article['plain_text']:
        fp.write(element['text'] + '\n\n')
