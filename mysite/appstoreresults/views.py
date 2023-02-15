from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import sqlite3 as lite
from .models import AppMetrics
import numpy as np
import sqlite3
import cgi
import json
from .forms import SearchResult


def index(request):

    try:
        sqliteConnection = sqlite3.connect('apptable.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")


        args=[]
        app_list =[]
        icon_list =[]
        id_list = []

        #if(val=='y'):
        sql = ("SELECT title, icon, appID, rating FROM apps ORDER BY rating desc limit 10".format(seq=','.join(['?']*len(args))))
        rows = cursor.execute(sql, args)
        for row in rows:
            print(row)
            icon_list.append(row[0]) #img
            app_list.append(row[3]) #app name
            id_list.append(row[2])

        # template = loader.get_template('index.html')
       
        res = {app_list[i]: [icon_list[i], id_list[i]] for i in range(len(app_list))}
        print(res)
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
               'appIcon': '../static/media/clue-icon.png',
               'overallScore': 83,
               'thirdPartyScore': 80,
               'dataEncryptionScore': 75,
               'sensitiveDataScore': 100,
               'transparencyScore': 50}

    return HttpResponse(template.render(context, request))

def scorecard(request, appID=None):
    # data = AppM3.objects.all()

    template = loader.get_template("scorecard.html")
    context = {'date': 'Feb 7, 2023',
               'title': "Clue Period & Cycle Tracker",
               'downloads': '10M+ downloads',
               'appIcon': '../static/media/clue-icon.png',
               'overallScore': 83,
               'thirdPartyScore': 80,
               'dataEncryptionScore': 75,
               'sensitiveDataScore': 100,
               'transparencyScore': 50}

    try:
        sqliteConnection = sqlite3.connect('apptable.db')
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        cursor = sqliteConnection.execute("SELECT * FROM apps WHERE appID like ?", ("%" + appID + "%",))
        res = cursor.fetchall()
        
        if len(res) != 0:
            print(dict(res[0]))
            app = res[0]
            context = {'date': 'Feb 7, 2023',
                        'title': app['title'],
                        'downloads': f"{app['downloads']} downloads",
                        'appIcon': app['icon'],
                        'overallScore': 83,
                        'thirdPartyScore': 80,
                        'dataEncryptionScore': 75,
                        'sensitiveDataScore': 100,
                        'transparencyScore': 50}
            return HttpResponse(template.render(context, request))
                
                
        else:
            res = "App not found, try again"
            return HttpResponse(template.render(context, request))

    #cannot connect:
    except sqlite3.Error as error:
        print("Failed to connect", error)
        str = "app not found"
        return HttpResponse(template.render(context, request))


def search(request):
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        form = SearchResult(request.POST)
        if form.is_valid():
            query = form.cleaned_data['your_search']

            try:
                sqliteConnection = sqlite3.connect('apptable.db')
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                cursor = sqliteConnection.execute("SELECT title, icon, appID FROM apps WHERE title LIKE ?", ("%" + query + "%",))
                res = cursor.fetchall()
                
                if len(res) != 0:
                    app_list =[]
                    icon_list =[]
                    id_list = []

                    for r in res:
                        icon_list.append(r[0]) 
                        app_list.append(r[1])
                        id_list.append(r[2])
                        output = {app_list[i]: [icon_list[i], id_list[i]] for i in range(len(app_list))}
                    
                    return render(request, 'search.html', {'output': output})
                        
                        
                else:
                    res = "App not found, try again"
                    return render(request, 'search.html', {'form':res})

            #cannot connect:
            except sqlite3.Error as error:
                print("Failed to connect", error)
                str = "app not found"
                return render(request, 'search.html', {'form': str})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchResult()
        return render(request, 'search.html', {'form': form})


def submit(request):
    return render(request, "submit.html")

