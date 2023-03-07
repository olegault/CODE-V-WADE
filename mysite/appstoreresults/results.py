#to access table: 'sqlite3 app' in terminal 
#remember to use python3 
import sqlite3
from google_play_scraper import search, Sort, permissions, app
import string
import random
import numpy as np


#connect to db 
try:
    sqliteConnection = sqlite3.connect('db-final.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    #get results
    val = input("Enter Keyword to Search Google Play Store: ")

    result = search(
        val,
        lang="en",  # defaults to 'en'
        country="us",  # defaults to 'us'
        n_hits=30  # defaults to 30 (= Google's maximum)
    )

    r = result[0]

    #appid, title, etc
    keys = r.keys()

    #get all values
    for row in result:
        values = row.values()
        arr = []
        for v in values:
            arr.append(v)
        app_search = arr[0] 

        #get app details/information 
        result_details = app(
            app_search,
            lang="en",
            country="us"
        )
        rd_keys = result_details.keys()
        rd_values = result_details.values()

        arr_details = []
        N = 5
        unique_id = ''.join(random.choices(string.digits, k=N))


        #PREVENT DUPLICATES
        cursor.execute("SELECT UID, Name FROM 'App Matrix'")
        output = cursor.fetchall()
        res = np.array(output)

        for n in res:
            #check UID 
            if (n[0] ==int(unique_id)):
                unique_id = ''.join(random.choices(string.digits, k=5))

            #check name
            cursor.execute("SELECT Name from 'App Matrix' where Name like 'n[1]'")
            yea = cursor.fetchall()
            if(len(yea)!=0):
                print("REPEATS")
                exit(1)
                #need to remove from inserting instead of just exiting

    
        #UID
        arr_details.append(int(unique_id))
        for v in rd_values:
        #UID, title, installs, score, developer, devID, devEmail, devWeb, 
        #devAddress, privacyPolicy, genreID, icon, released, updated, appID, URL
            arr_details.append(v)

        sql = cursor.execute('''INSERT or REPLACE INTO 'App Matrix' ('UID', 'Name', 'Downloads', 'Rating', 'Developer', 'devID', 'devEmail', 'devWeb', 'devAddress', 'privacyPolicy', 'Genre', 'icon', 'released', 'updated', 'appID', 'url') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', arr_details)
        sqliteConnection.commit()
        print("Record inserted successfully into apps table ", cursor.rowcount)

    cursor.close()


#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")








