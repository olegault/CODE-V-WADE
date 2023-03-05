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

def bool_to_text(b):
    if b:
        return("Yes")
    else:
        return("No")

def translate_score(score):
    if score > 89:
        return ("Great", "score-great")
    if score > 69:
        return ("Good", "score-good")
    if score > 49:
        return ("Okay", "score-okay")
    if score > 29:
        return ("Subpar", "score-subpar")
    else:
        return ("Bad", "score-bad")

def index(request):

    try:
        sqliteConnection = sqlite3.connect('apptable.db')
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")


        args=[]
        app_list =[]
        icon_list =[]
        id_list = []
        score_list = []

        #if(val=='y'):
        sql = ("SELECT title, icon, appID, overallScore, rating FROM apps ORDER BY rating desc limit 10".format(seq=','.join(['?']*len(args))))
        rows = cursor.execute(sql, args)
        for row in rows:
            print(row)
            icon_list.append(row['icon']) #img
            app_list.append(row['title']) #app name
            id_list.append(row['appID'])
            score_list.append(row['overallScore'])

        # template = loader.get_template('index.html')
       
        res = {app_list[i]: [icon_list[i], id_list[i], score_list[i]] for i in range(len(app_list))}
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
               'overallScore': 82,
               'overallDesc': 'Good',
               'overallClass': 'score-good',
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
            score_desc, score_class = translate_score(app["overallScore"])
            context = {'date': 'Feb 7, 2023',
                        'title': app['title'],
                        'downloads': f"{app['downloads']} downloads",
                        'appIcon': app['icon'],
                        'overallScore': app["overallScore"],
                        'overallDesc': score_desc,
                        'overallClass': score_class,

                        'thirdPartyScore': 80,
                        'shareAdvertisers': bool_to_text(app['shareAdvertisers']),
                        'shareLawEnforcement': bool_to_text(app['shareLawEnforcement']),
                        'shareDataBrokers': bool_to_text(app['shareDataBrokers']),
                        'shareHealthCareProvider': bool_to_text(app['shareHealthCareProvider']),
                        
                        'dataEncryptionScore': 75,
                        'encryptedTransit': bool_to_text(app['encryptedTransit']),
                        'encryptedOnDevice': bool_to_text(app['encryptedOnDevice']),
                        'encryptedMetadata': bool_to_text(app['encryptedMetadata']),

                        'sensitiveDataScore': 100,
                        'collectPII': bool_to_text(app['collectPII']),
                        'collectHealthInfo': bool_to_text(app['collectHealthInfo']),
                        'collectReproductiveInfo': bool_to_text(app['collectReproductiveInfo']),
                        'collectPeriodCalendarInfo': bool_to_text(app['collectPeriodCalendarInfo']),

                        'transparencyScore': 50,
                        'requestData': bool_to_text(app['requestData']),
                        'requestDeletion': bool_to_text(app['requestDeletion']),
                        'controlData': bool_to_text(app['controlData']),
                        'controlSharing': bool_to_text(app['controlSharing'])
                        }
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
                sqliteConnection.row_factory = sqlite3.Row
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                cursor = sqliteConnection.execute("SELECT title, icon, appID, overallScore FROM apps WHERE title LIKE ?", ("%" + query + "%",))
                res = cursor.fetchall()
                
                if len(res) != 0:
                    app_list =[]
                    icon_list =[]
                    id_list = []
                    score_list = []

                    for r in res:
                        icon_list.append(r['icon']) 
                        app_list.append(r['title'])
                        id_list.append(r['appID'])
                        score_list.append(r['overallScore'])
                        output = {app_list[i]: [icon_list[i], id_list[i], score_list[i]] for i in range(len(app_list))}
                    
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

def worldmap(request):
    #return sorted by region based on user selection 
    return render(request, "index.html")
