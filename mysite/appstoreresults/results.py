#add results from search into sqlite3 app table
#to access table: 'sqlite3 app' in terminal 
#remember to use python3 
import sqlite3
from google_play_scraper import search



#connect to db 
try:
    sqliteConnection = sqlite3.connect('apptable.db')
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
        print(arr[0])
        #sqlite_insert_query = '''INSERT INTO app ('appID', 'title', 'rating', 'genre', 'price', 'developer', 'downloads') VALUES (?,?,?,?,?,?,?)'''
        count = cursor.execute('''INSERT INTO apps ('appID', 'title', 'rating', 'genre', 'price', 'developer', 'downloads') VALUES (?,?,?,?,?,?,?)''', arr)
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







