from privpol import analyze_policy
from notify_packet_analysis import send_notification
from google_play_scraper import app
from pathlib import Path
import sqlite3

#file invoked when user clicks SUBMIT (after inputting the app store and/or priv pol urls)
#1. webscrape from api autocalled
#2. copy-paste URL from app store, which gets fed into NLP
#3. email PING gets sent to CVW email with info abt the app to prompt packet testing.

#EACH of 1,2 will output a binary array which each corresponds to questions (see metrics.txt) we use to decide score
#the qs for 3 will have a default of "0" until the packet testing is complete—@Miles can update site w new numbers


#a later workflow is a form to automatically update those numbers for miles, and a "not complete" tag for apps that dont have testing done yet

#last thing is to take a calculation of the total score (we can just do a basic "add all the value and multiply the sum by a nubmer for rn")
#then display

BASE_DIR = Path(__file__).resolve().parent.parent

def valid_url(url):
    if 'play.google.com/store/apps/' in url:
        try:
            package = url.split('id=')[1].split('&')[0]
            result = app(
                package,
                lang='en', # defaults to 'en'
                country='us' # defaults to 'us'
            )
            return result
        
        except BaseException as e:
            print(e)
        
    return None

def update_db_entry(package, metrics):
    sqliteConnection = sqlite3.connect('db-final.db')
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    for metric in metrics:
        if metrics[metric]: val = 1
        else: val = 0

        print(metric, val, package)
        cursor = sqliteConnection.execute(f'''UPDATE 'App Matrix' SET {metric}=? WHERE appID="?"''', (val, package))
    return True


def calculate_m3(url):

    app_info = valid_url(url)
    if not app_info:
        return False

    package = url.split('id=')[1].split('&')[0]
    send_notification(url)

    metrics = analyze_policy(app_info['privacyPolicy'])
    if metrics:
        res = update_db_entry(package, metrics)
        print("Updated entries: " , metrics)
    return True
    

if __name__ == '__main__':
    url = input("Enter Play Store Link: ")
    calculate_m3(url)

    val = 0 #default for score




