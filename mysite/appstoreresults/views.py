from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from appstoreresults.m3 import valid_url, calculate_m3
import sqlite3 as lite
from .models import AppMetrics
import numpy as np
import sqlite3
import cgi
import json
from .forms import SearchResult, SubmitResult

DB_FILEPATH = './appstoreresults/db-final.db'

def bool_to_text(b):
    if b:
        return("Yes")
    else:
        return("No")

def translate_score(score):
    if not score:
        score = -1
    if score > 89:
        return ("Great", "score-great")
    if score > 69:
        return ("Good", "score-good")
    if score > 49:
        return ("Okay", "score-okay")
    if score > 29:
        return ("Subpar", "score-subpar")
    if score > -1:
        return ("Bad", "score-bad")
    else:
        return ("No Score", "score-none")

def index(request):

    try:
        sqliteConnection = sqlite3.connect(DB_FILEPATH)
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")


        args=[]
        app_list =[]
        icon_list =[]
        id_list = []
        score_list = []

        #if(val=='y'):
        sql = ('SELECT Name, Icon, appID, overallScore, Rating FROM "App Matrix" ORDER BY Downloads desc limit 10'.format(seq=','.join(['?']*len(args))))
        rows = cursor.execute(sql, args)
        print("here")

        for row in rows:
            # print(row)
            icon_list.append(row['Icon']) #img
            app_list.append(row['Name']) #app name
            id_list.append(row['appID'])
            score_list.append(row['overallScore'])

       
        res = {app_list[i]: [icon_list[i], id_list[i], score_list[i]] for i in range(len(app_list))}
        # print(res)
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
               'title': "Could not load",
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
               'title': "Could not load",
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
        sqliteConnection = sqlite3.connect(DB_FILEPATH)
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        cursor = sqliteConnection.execute('SELECT * FROM "App Matrix" WHERE appID like ?', ("%" + appID + "%",))
        res = cursor.fetchall()    
        
        if len(res) != 0:
            print(dict(res[0]))
            app = res[0]
            score_desc, score_class = translate_score(app["overallScore"])
            context = {'date': 'Feb 7, 2023',
                        'title': app['Name'],
                        'downloads': f"{app['Downloads']} downloads",
                        'appIcon': app['Icon'],
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
                sqliteConnection = sqlite3.connect(DB_FILEPATH)
                sqliteConnection.row_factory = sqlite3.Row
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                cursor = sqliteConnection.execute("SELECT Name, Icon, appID, overallScore, Rating FROM 'App Matrix' WHERE Name LIKE ?", ("%" + query + "%",))
                res = cursor.fetchall()
                
                if len(res) != 0:
                    app_list =[]
                    icon_list =[]
                    id_list = []
                    score_list = []

                    for r in res:
                        icon_list.append(r['Icon']) 
                        app_list.append(r['Name'])
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
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        form = SubmitResult(request.POST)
        if not form.is_valid():
            return render(request, 'submit.html')
        
        url = form.cleaned_data['submit_url']
        app_info = valid_url(url)

        if not app_info:
            return render(request, 'submit.html')
        
        if not calculate_m3(url):
            return render(request, 'submit.html')
        
        template = loader.get_template("submitdone.html")
        return HttpResponse(template.render(app_info, request))

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request, 'submit.html')

def worldmap(request, default_region=None):
    #return sorted by region based on user selection 
    chosen = default_regions["0"]["name"]
    if(chosen == '0'):
        return render(request, "index.html")

    print(chosen)
    #getelementbyID
    #worldmap.js has default_regions 0-5

    return render(request, "index.html")

def submitdone(request):
    return render(request, "submitdone.html")
