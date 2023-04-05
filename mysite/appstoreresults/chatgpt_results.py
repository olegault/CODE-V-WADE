import sqlite3
from google_play_scraper import app
import numpy as np

try:
    sqliteConnection = sqlite3.connect('db-final.db')
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")


    privpol = 'http://www.smsrobot.com/privacypolicy_period.html'

    analysis = "This is a privacy policy for Lilly Tracker, which is a website and mobile application that provides backup services for storing personal information related to menstruation, fertility, and health. The policy states that the company is committed to protecting and respecting the privacy of its users and will only collect and process personal information in accordance with applicable privacy laws. The policy also includes information about the types of data that may be collected, such as account information, personal data, contact details, technical or other details about the device used to access the Services, and details of the use of the Services. The company states that it will use this data to provide backup services in a reliable and secure manner, present content effectively, provide requested information or services, perform contractual obligations, and notify users about changes to the Services. The policy notes that communications via the Services may reveal certain personal information to other users and that the company is not responsible for the activities of other users or third parties. The policy also explains that the company may store data outside of the European Economic Area (EEA) and that by submitting personal data, users agree to this transfer and processing of data."


    citations = ""


#add results to table
    cursor.execute('''UPDATE 'App Matrix' SET 'chatgpt_analysis'=?, 'chatgpt_citations'=? WHERE privacyPolicy = ?''', (analysis, citations, privpol))
    sqliteConnection.commit()
    cursor.close()

#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")

