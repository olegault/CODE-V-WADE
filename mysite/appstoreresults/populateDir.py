import sqlite3
from google_play_scraper import app
import numpy as np

try:
    sqliteConnection = sqlite3.connect('db-final.db')
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")


    cursor.execute("SELECT Name FROM 'App Matrix'")
    output = cursor.fetchall()
    res = np.array(output)
    ones = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    for n in res:
        print(n[0])                  
        cursor.execute('''UPDATE 'App Matrix' SET 'shareAdvertisers'=?, 'shareLawEnforcement'=?, 'shareDataBrokers'=?, 'shareHealthCareProvider'=?, 'encryptedTransit'=?, 'encryptedOnDevice'=?, 'encryptedMetadata'=?, 'requestData'=?, 'requestDeletion'=?,'controlData'=?,'controlSharing'=? WHERE Name = ?''', (*ones, n[0]))
        sqliteConnection.commit()
    cursor.close()

#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")



