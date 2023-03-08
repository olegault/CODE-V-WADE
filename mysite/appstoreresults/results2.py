import sqlite3
from google_play_scraper import permissions

#connect to db 
try:
    sqliteConnection = sqlite3.connect('db.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    cursor.execute('''SELECT appID FROM 'App Matrix' ''')
    rows = cursor.fetchall()
    
    for row in rows:
        result = permissions(
            row[0],
            lang='en', # defaults to 'en'
            country='us', # defaults to 'us'
        )

        cursor.execute('''INSERT INTO 'App Matrix' ('permissions') VALUES (?)''', result)
        sqliteConnection.commit()
        print(result)


        INSERT INTO apps [('permissions')] 
        SELECT appID
        FROM apps
        [WHERE appID = result];


    for row in result:
        values = row.values()
        arr = []
        for v in values:
            arr.append(v)
        print(arr[0])
        count = cursor.execute('''INSERT INTO apps ('permissions') VALUES (?)''', result)
        sqliteConnection.commit()
        print("Record inserted successfully into apps table ", cursor.rowcount)
    cursor.close()


#cannot connect:
except sqlite3.Error as error:
    print("Failed to get data from sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")
