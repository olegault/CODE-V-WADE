import numpy as np
import sqlite3
from google_play_scraper import search

try:
    sqliteConnection = sqlite3.connect('apptable.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    #get results
    val = input("Update Top Search Results? Y/N\n")

    if(val=='y'):
        args=[]
        title=[]
        icon=[]
        sql = ("SELECT title, rating, icon FROM apps ORDER BY rating desc limit 10".format(seq=','.join(['?']*len(args))))
        rows = cursor.execute(sql, args)
        for row in rows:
            icon.append(row[0])
            title.append(row[1])

        np.savetxt("top_apps.txt",icon, fmt='%s')
        np.savetxt("top_apps_title.txt",title, fmt='%s')


        html = "<html><body>"
        for item in title:
            html += "<p>" + str(item) + "</p>"
        html += "</body></html>"
        print(html)



    else:
        cursor.close()


#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")

