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
import datetime
import pycountry

DB_FILEPATH = './appstoreresults/db-final.db'

def int_to_text(i):
    if i == 1:
        return("Yes")
    elif i == 0:
        return("No")
    else:
        return("Under Review")

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
    
def under_review(score):
    if score == -1:
        return 'Under Review'
    return score

def index(request):

    try:
        sqliteConnection = sqlite3.connect(DB_FILEPATH)
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")


        #COUNTRIES
        all_countries = list(pycountry.countries)
        # create a list of tuples with the country name and code
        countries_list = [(country.name, country.alpha_2) for country in all_countries]
        # sort the list by country name
        countries_list.sort()


        args=[]
        app_list =[]
        icon_list =[]
        id_list = []
        score_list = []

        #if(val=='y'):
        sql = ('SELECT Name, Icon, UID, overallScore, Rating FROM "App Matrix" ORDER BY Downloads desc limit 10'.format(seq=','.join(['?']*len(args))))
        rows = cursor.execute(sql, args)
        print("here")

        for row in rows:
            # print(row)
            icon_list.append(row['Icon']) #img
            app_list.append(row['Name']) #app name
            id_list.append(row['UID'])
            score_list.append(row['overallScore'])

       
        res = {app_list[i]: [icon_list[i], id_list[i], score_list[i]] for i in range(len(app_list))}
        # print(res)
        return render(request, 'index.html', {'res':res, 'countries': countries_list})

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


        cursor = sqliteConnection.execute('SELECT * FROM "App Matrix" WHERE UID = ?', (appID,))
        res = cursor.fetchall()    

        if len(res) != 0:
            print(dict(res[0]))
            app = res[0]
            print(app['UID'])
            datetime_value = datetime.datetime.utcfromtimestamp(app['updated'])
            score_desc, score_class = translate_score(app["overallScore"])
            share_desc, share_class = translate_score(app["thirdPartySharingScore"])
            encryption_desc, encryption_class = translate_score(app["dataEncryptionScore"])
            sensitive_desc, sensitive_class = translate_score(app["sensitiveDataScore"])
            transparency_desc, transparency_class = translate_score(app["transparencyScore"])

            context = {'date': datetime_value,
                        'title': app['Name'],
                        'downloads': f"{app['Downloads']} downloads",
                        'appIcon': app['Icon'],
                        'overallScore': under_review(app["overallScore"]),
                        'overallDesc': score_desc,
                        'overallClass': score_class,

                        'thirdPartyScore': under_review(app['thirdPartySharingScore']),
                        'thirdPartyDesc': share_desc,
                        'thirdPartyClass': share_class,
                        'shareAdvertisers': int_to_text(app['shareAdvertisers']),
                        'shareLawEnforcement': int_to_text(app['shareLawEnforcement']),
                        'shareDataBrokers': int_to_text(app['shareDataBrokers']),
                        'shareHealthCareProvider': int_to_text(app['shareHealthCareProvider']),
                        
                        'dataEncryptionScore': under_review(app['dataEncryptionScore']),
                        'encryptionDesc': encryption_desc,
                        'encryptionClass': encryption_class,
                        'encryptedTransit': int_to_text(app['encryptedTransit']),
                        'encryptedOnDevice': int_to_text(app['encryptedOnDevice']),
                        'encryptedMetadata': int_to_text(app['encryptedMetadata']),

                        'sensitiveDataScore': under_review(app['sensitiveDataScore']),
                        'sensitiveDataDesc': sensitive_desc,
                        'sensitiveDataClass': sensitive_class,
                        'collectPII': int_to_text(app['collectPII']),
                        'collectHealthInfo': int_to_text(app['collectHealthInfo']),
                        'collectReproductiveInfo': int_to_text(app['collectReproductiveInfo']),
                        'collectPeriodCalendarInfo': int_to_text(app['collectPeriodCalendarInfo']),

                        'transparencyScore': under_review(app['transparencyScore']),
                        'transparencyDesc': transparency_desc,
                        'transparencyClass': transparency_class,
                        'requestData': int_to_text(app['requestData']),
                        'requestDeletion': int_to_text(app['requestDeletion']),
                        'controlData': int_to_text(app['controlData']),
                        'controlSharing': int_to_text(app['controlSharing'])
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

def countries(request):
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
            
            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
                return render(request, "index.html")
    
    return render(request, "index.html")

def submitdone(request):
    return render(request, "submitdone.html")


