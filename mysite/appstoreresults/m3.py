#import appstoreresults.privpol
#import appstoreresults.notify_packet_analysis
#from google_play_scraper import app
from pathlib import Path
import sqlite3
import os

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
DB_FILEPATH = os.path.join('db-final.db')

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
    sqliteConnection = sqlite3.connect(DB_FILEPATH)
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    cursor = sqliteConnection.execute("SELECT * FROM 'App Matrix' WHERE Name LIKE ?", ("%" + package + "%",))
    res = cursor.fetchall()
    app_db = res[0]
    print(app_db['UID'])

    for metric in metrics:
        if metrics[metric]: val = 1
        else: val = 0

        print(metric, val, package)
        try:
            cursor = sqliteConnection.execute(f'''UPDATE 'App Matrix' SET {metric}=? WHERE UID = ?''', (val, app_db['UID']))
            sqliteConnection.commit()
        except BaseException as e:
            print(e)
    return True


def calculate_m3(url):

    app_info = valid_url(url)
    if not app_info:
        return False

    package = url.split('id=')[1].split('&')[0]
    appstoreresults.notify_packet_analysis.send_notification(url)

    metrics = appstoreresults.privpol.analyze_policy(app_info['privacyPolicy'])
    if metrics:
        res = update_db_entry(app_info['title'], metrics)
        print("Updated entries: " , metrics)
    return True
    

if __name__ == '__main__':
    url = input("Enter Play Store Link: ")
    calculate_m3(url)

    val = 0 #default for score




