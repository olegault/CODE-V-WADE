from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import sqlite3 as lite
from .models import AppMetrics
import numpy as np
import sqlite3

def index(request):

    try:
        sqliteConnection = sqlite3.connect('apptable.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")


        args=[]
        app_list =[]
        icon_list =[]
        app_dict = {}
        #if(val=='y'):
        sql = ("SELECT title, icon, rating FROM apps ORDER BY rating desc limit 10".format(seq=','.join(['?']*len(args))))
        rows = cursor.execute(sql, args)
        for row in rows:
            icon_list.append(row[0]) #img
            app_list.append(row[2]) #app name

        template = loader.get_template('index.html')
       
        res = {app_list[i]: icon_list[i] for i in range(len(app_list))}

        return render(request, 'index.html', {'res':res})

    #cannot connect:
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
        return render(request, "index.html")



def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def writing4(request):
    return render(request, "writing4.html")

def scorecard(request):
    # data = AppM3.objects.all()

    template = loader.get_template("scorecard.html")
    context = {'date': 'Feb 7, 2023',
               'title': "Clue Period & Cycle Tracker",
               'downloads': '10M+ downloads',
               'appIcon': 'Hey!',
               'overallScore': 83,
               'thirdPartyScore': 80,
               'dataEncryptionScore': 75,
               'sensitiveDataScore': 100,
               'transparencyScore': 50}

    return HttpResponse(template.render(context, request))


def search(request):
    template = loader.get_template("search.html")  
    return render(request, "search.html")

def submit(request):
    template = loader.get_template("submit.html")  
    return render(request, "submit.html")