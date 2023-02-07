from google_play_scraper import app
import urllib.request

link = input("Enter Play Store Link: ")
# link = 'https://play.google.com/store/apps/details?id=com.clue.android&hl=en_US&gl=US'

package = link.split('id=')[1].split('&')[0]
print(package)

result = app(
    package,
    lang='en', # defaults to 'en'
    country='us' # defaults to 'us'
)

policy_link = result['privacyPolicy']
#print(policy_link)

uf = urllib.request.urlopen(policy_link)

html = uf.read



