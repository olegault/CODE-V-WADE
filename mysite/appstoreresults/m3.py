import appstoreresults.privpol
import appstoreresults.notify_packet_analysis
from google_play_scraper import app
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
DB_FILEPATH = os.path.join(BASE_DIR, 'appstoreresults/db-final.db')

pos_neg_metrics = {'shareAdvertisers': -1,
                   'shareLawEnforcement': -1,
                   'shareDataBrokers': -1,
                   'shareHealthCareProvider': -1,
                   'encryptedTransit': 1,
                   'encryptedOnDevice': 1,
                   'encryptedMetadata': 1,
                   'collectPII': -1,
                   'collectHealthInfo': -1,
                   'collectReproductiveInfo': -1,
                   'collectPeriodCalendarInfo': -1,
                   'requestData': 1,
                   'requestDeletion': 1,
                   'controlData': 1,
                   'controlSharing': 1}

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

def calc_score(cols, metrics_old):
    sm = 0
    metrics = {k: v for k, v in metrics_old.items() if v != -1}
    if len(metrics) < 1:
        return -1

    for c in metrics:
        if metrics[c] == -1:
            del metrics[c]
            continue

    for c in metrics:
        if cols[c] == 1 and metrics[c] == 1:
            sm += 1
        if cols[c] == -1 and metrics[c] == 0:
            sm += 1

    score = (sm / len(metrics) * 100)
    return round(score)

def get_sharing_score(app_row):
    metrics = {'shareAdvertisers': app_row['shareAdvertisers'],
               'shareLawEnforcement': app_row['shareLawEnforcement'],
               'shareDataBrokers': app_row['shareDataBrokers'],
               'shareHealthCareProvider': app_row['shareHealthCareProvider']}
    return calc_score(pos_neg_metrics, metrics)

def get_encryption_score(app_row):
    metrics = {'encryptedTransit': app_row['encryptedTransit'],
            #    'encryptedOnDevice': app_row['encryptedOnDevice'],
            #    'encryptedMetadata': app_row['encryptedMetadata']
               }
    return calc_score(pos_neg_metrics, metrics)

def get_sensitive_score(app_row):
    metrics = {'collectPII': app_row['collectPII'],
               'collectHealthInfo': app_row['collectHealthInfo'],
               'collectReproductiveInfo': app_row['collectReproductiveInfo'],
               'collectPeriodCalendarInfo': app_row['collectPeriodCalendarInfo']}
    return calc_score(pos_neg_metrics, metrics)

def get_transparency_score(app_row):
    metrics = {'requestData': app_row['requestData'],
               'requestDeletion': app_row['requestDeletion'],
               'controlData': app_row['controlData'],
               'controlSharing': app_row['controlSharing']}
    return calc_score(pos_neg_metrics, metrics)

def get_overall_score(app_row):
    metrics = {'shareAdvertisers': app_row['shareAdvertisers'],
               'shareLawEnforcement': app_row['shareLawEnforcement'],
               'shareDataBrokers': app_row['shareDataBrokers'],
               'shareHealthCareProvider': app_row['shareHealthCareProvider'],
               'encryptedTransit': app_row['encryptedTransit'],
            #    'encryptedOnDevice': app_row['encryptedOnDevice'],
            #    'encryptedMetadata': app_row['encryptedMetadata'],
               'collectPII': app_row['collectPII'],
               'collectHealthInfo': app_row['collectHealthInfo'],
               'collectReproductiveInfo': app_row['collectReproductiveInfo'],
               'collectPeriodCalendarInfo': app_row['collectPeriodCalendarInfo'],
               'requestData': app_row['requestData'],
               'requestDeletion': app_row['requestDeletion'],
               'controlData': app_row['controlData'],
               'controlSharing': app_row['controlSharing']}
    return calc_score(pos_neg_metrics, metrics)

def update_scores(app_title):
    print('Updating scores')
    sqliteConnection = sqlite3.connect(DB_FILEPATH)
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    cursor = sqliteConnection.execute("SELECT * FROM 'App Matrix' WHERE Name LIKE ?", ("%" + app_title + "%",))
    res = cursor.fetchall()
    app_row = res[0]
    print(app_row['overallScore'])

    overall = get_overall_score(app_row)
    sharing = get_sharing_score(app_row)
    encryption = get_encryption_score(app_row)
    sensitive = get_sensitive_score(app_row)
    transparency = get_transparency_score(app_row)

    try:
        cursor = sqliteConnection.execute(f'''UPDATE 'App Matrix' SET overallScore=?, thirdPartySharingScore=?, dataEncryptionScore=?, sensitiveDataScore=?, transparencyScore=? WHERE UID = ?''', 
                                          (overall, sharing, encryption, sensitive, transparency, app_row['UID']))
        sqliteConnection.commit()
        print('committed')
    except BaseException as e:
        print(e)

def calculate_m3(url):

    app_info = valid_url(url)
    if not app_info:
        return False

    package = url.split('id=')[1].split('&')[0]
    appstoreresults.notify_packet_analysis.send_notification(url)

    privpol_metrics = appstoreresults.privpol.analyze_policy(app_info['privacyPolicy'])
    if privpol_metrics:
        res = update_db_entry(app_info['title'], privpol_metrics)
        print("Updated entries: " , privpol_metrics)

    update_scores(app_info['title'])
    

if __name__ == '__main__':
    url = input("Enter Play Store Link: ")
    calculate_m3(url)
    # print(get_sharing_score())
    val = 0 #default for score




