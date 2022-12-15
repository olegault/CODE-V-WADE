from django.shortcuts import render
import sqlite3 as lite


def index(request):
    return render(request, "index.html")

def alphademo(request):
    #connect to db 
    #
    #try:
    #    sqliteConnection = sqlite3.connect('apptable.db')
    #    cursor = sqliteConnection.cursor()
    #    print("Successfully Connected to SQLite")
    #    arr = []
    #    result = cursor.execute('''SELECT title FROM apps''', arr)
    #    sqliteConnection.commit()

        #get all values
        #for row in result:
        #    print(row)
            
        #cursor.close()

    #cannot connect:
    #except sqlite3.Error as error:
    #    print("Failed to get data from sqlite table", error)
    #finally:
    #    if sqliteConnection:
    #        sqliteConnection.close()
    #        print("The SQLite connection is closed")

    #results = apptable.db.objects.all()
    return render(request, "alphademo.html")

def about(request):
    return render(request, "about.html")

def scorecard(request):
    return render(request, "scorecard.html")

def contact(request):
    return render(request, "contact.html")

def writing4(request):
    return render(request, "writing4.html")

