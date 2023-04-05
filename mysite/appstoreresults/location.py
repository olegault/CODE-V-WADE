import sqlite3
from google_play_scraper import app
import numpy as np

try:
    sqliteConnection = sqlite3.connect('db-final.db')
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")


    cursor.execute("SELECT devAddress FROM 'App Matrix'")
    output = cursor.fetchall()
    res = np.array(output)

    loc_arr = ["NA", "None", "SA", "AS", "EU", "EU", "None", "EU", "AS", "None", "AS", "None", "EU", "AS", "None", "EU", "EU", "AS", "None", "None", "None", "NA", "EU", "AS", "None", "NA", "None", "EU", "EU", "None", "NA", "None", "EU", "None", "None", "NA", "NA", "AS", "EU", "None", "None", "EU", "AS", "None", "None", "NA", "None", "NA", "NA", "EU", "NA",
                "EU", "NA", "AS", "None", "None", "None", "None", "NA", "NA", "EU", "EU", "None", "None", "AS", "NA", "None", "None", "NA", "NA", "EU", "AS", "NA", "NA", "None",
                "None", "EU", "None", "EU", "AS", "AS", "NA", "NA", "EU", "EU", "None", "None", "None", "EU", "EU", "EU", "None", "EU", "NA", "NA", "NA", "EU", "None", "None", "AUS", "EU", 
                "None", "EU", "AS", "EU", "AUS", "None", "NA", "NA", "None", "None", "None", "NA", "NA", "None"]

    print("loc", loc_arr[3])
    i = 0;

    #location finder 
    for n in res:
        cursor.execute('''UPDATE 'App Matrix' SET 'region'=? WHERE devAddress = ?''', (loc_arr[i], n[0]))
        sqliteConnection.commit()
        print(n[0],"\n") 
        i=i+1  
    cursor.close()

#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")

