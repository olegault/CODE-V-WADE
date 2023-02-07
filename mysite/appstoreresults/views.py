from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import sqlite3 as lite
from .models import AppM3
import numpy as np
import sqlite3

def index(request):

    try:
        sqliteConnection = sqlite3.connect('apptable.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        #get results
        #val = input("Update Top Search Results? Y/N\n")
        args=[]
        app_list =[]
        icon_list =[]
        context = {}
        #if(val=='y'):
        sql = ("SELECT title, icon, rating FROM apps ORDER BY rating desc limit 10".format(seq=','.join(['?']*len(args))))
        rows = cursor.execute(sql, args)
        for row in rows:
            icon_list.append(row[0]) #img
            app_list.append(row[2]) #app name

        #else:
        #    cursor.close()

        template = loader.get_template('index.html')

        #context = {'app_list': app_list}
       

        #return HttpResponse(template.render(context, request))
        return render(request, 'index.html', {'app_list':app_list, 'icon_list':icon_list})


    #cannot connect:
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
        return render(request, "index.html")


def alphademo(request):
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
