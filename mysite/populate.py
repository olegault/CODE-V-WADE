import sqlite3
import random

#connect to db 
try:
    sqliteConnection = sqlite3.connect('apptable.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    
    for i in range(149):
        arr = []
        for r in range(19):
            k = random.randint(0, 1) # decide on a k each time the loop runs
            arr.append(k)        

        print(arr)
        
        count = cursor.execute('''UPDATE apps SET('thirdPartySharingScore',
                                                    'shareAdvertisers',
                                                    'shareLawEnforcement',
                                                    'shareDataBrokers',
                                                    'shareHealthCareProvider',
                                                    'dataEncryptionScore',
                                                    'encryptedTransit',
                                                    'encryptedOnDevice',
                                                    'encryptedMetadata',
                                                    'sensitiveDataScore', 
                                                    'collectPII',
                                                    'collectHealthInfo',
                                                    'collectReproductiveInfo',
                                                    'collectPeriodCalendarInfo',
                                                    'transparencyScore',
                                                    'requestData',
                                                    'requestDeletion',
                                                    'controlData',
                                                    'controlSharing') = (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', arr)
        sqliteConnection.commit()
    
    cursor.close()

#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")