#import requests
import sqlite3
from google_play_scraper import app

def analyze_policy(policy_url):
    r = requests.post(

        "https://api.deepai.org/api/summarization",
        data={
            'text': policy_url,
        },
        headers={'api-key': '62094660-0461-4c8a-9885-7243213f3b81'}
    )

    text = r.text
    metrics = {"collectPII": False,
            "collectHealthInfo": False,
            "collectMedicationInfo" : False,
            "collectReproductiveInfo": False,
            "collectPeriodCalendarInfo": False,
            "requestDeletion": False,
            "controlData": False,
            "controlSharing": False}

    if "identifying information" in text:
        metrics['collectPII'] = True
    if "non-reproductive" in text:
        metrics['collectHealthInfo'] = True
    if "medication" in text:
        metrics['collectMedicationInfo'] = True
    if "period calendar" in text:
        metrics['collectPeriodCalendarInfo'] = True
    if "deletion" in text:
        metrics['requestDeletion'] = True
    if "control" in text:
        metrics['controlData'] = True
    if "control" and "shared" in text:
        metrics['controlSharing'] = True

    #ret arr
    # print(r.json())
    print(metrics)
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
        print(res)
            #for n in res:
            #    analyze_policy(policy)

    #cannot connect:
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



