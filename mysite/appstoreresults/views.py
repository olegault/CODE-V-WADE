from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import sqlite3 as lite
from .models import AppM3

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

def apppage(request):
    # data = AppM3.objects.all()

    template = loader.get_template("scorecard.html")
    context = {'title': "Clue Period & Cycle Tracker",
               'downloads': '10M+ downloads'}

    return HttpResponse(template.render(context, request))
