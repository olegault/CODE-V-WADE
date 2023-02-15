from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import sqlite3 as lite
from .models import AppMetrics
import numpy as np
import sqlite3
import cgi
from .forms import SearchResult


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
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        form = SearchResult(request.POST)
        if form.is_valid():
            query = form.cleaned_data['your_search']

            try:
                sqliteConnection = sqlite3.connect('apptable.db')
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                cursor = sqliteConnection.execute("SELECT title, icon FROM apps WHERE title LIKE ?", ("%" + query + "%",))
                res = cursor.fetchall()
                
                if len(res) != 0:
                    app_list =[]
                    icon_list =[]

                    for r in res:
                        icon_list.append(r[0]) 
                        app_list.append(r[1])
                        output = {app_list[i]: icon_list[i] for i in range(len(app_list))}
                    
                    return render(request, 'search.html', {'output':output})
                        
                        
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



