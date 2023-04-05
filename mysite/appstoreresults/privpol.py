import sqlite3
from google_play_scraper import app
import numpy as np
import requests

def scrape_policy(url):
    package = link.split('id=')[1].split('&')[0]
    print(package)

    result = app(
        package,
        lang='en', # defaults to 'en'
        country='us' # defaults to 'us'
    )



    policy_link = result['privacyPolicy']

def analyze_policy(policy_url):
    r = requests.post(

        "https://api.deepai.org/api/summarization",
        data={
            'text': policy_url,
        },
        headers={'api-key': '62094660-0461-4c8a-9885-7243213f3b81'}
    )

    text = r.text
    metrics = {"collectPII": 0,
            "shareLawEnforcement":0,
            "shareAdvertisers":0,
            "shareHealthCare":0,
            "collectHealthInfo": 0,
            "collectMedicationInfo" : 0,
            "collectReproductiveInfo": 0,
            "collectPeriodCalendarInfo": 0,
            "requestDeletion": 0,
            "controlData": 0,
            "controlSharing": 0}

    if "identifying information" in text:
        metrics['collectPII'] = 1
    if "law enforcement" not in text:
        metrics['shareLawEnforcement'] = 1
    if "prohibit sharing with advertisers" in text:
        metrics['shareAdvertisers'] = 1
    if "share with partner organizations" in text:
        metrics['shareHealthCare'] = 1
    if "non-reproductive" in text:
        metrics['collectHealthInfo'] = 1 
    if "medication" in text:
        metrics['collectMedicationInfo'] = 1
    if "period calendar" in text:
        metrics['collectPeriodCalendarInfo'] = 1
    if "deletion" in text:
        metrics['requestDeletion'] = 1
    if "control" in text:
        metrics['controlData'] = 1
    if "control" and "shared" in text:
        metrics['controlSharing'] = 1

    #ret arr
    # print(r.json())
    return metrics

if __name__ == '__main__':

    try:
        sqliteConnection = sqlite3.connect('db-final.db')
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")


        cursor.execute("SELECT privacyPolicy FROM 'App Matrix'")
        output = cursor.fetchall()
        res = np.array(output)
        for n in res:
            arr = {}
            arr = analyze_policy(n)
            keys = arr.keys()
            values = list(arr.values())
            print(values)                  
            cursor.execute('''UPDATE 'App Matrix' SET 'collectPII'=?, 'collectHealthInfo'=?, 'collectMedicationInfo'=?, 'collectReproductiveInfo'=?, 'collectPeriodCalendarInfo'=?, 'requestDeletion'=?, 'controlData'=?, 'controlSharing'=? WHERE privacyPolicy = ?''', (*values, n[0]))
            sqliteConnection.commit()
        cursor.close()

    #cannot connect:
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



