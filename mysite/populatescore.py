import sqlite3
import random

#connect to db 
try:
    sqliteConnection = sqlite3.connect('apptable.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    
    for i in range(150):
        val = random.randint(30, 95) 
        print(val)
        cursor = sqliteConnection.execute('''UPDATE apps SET('overallScore') = (?)''', (val,))
        
    sqliteConnection.commit()
    cursor.close()

#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")


