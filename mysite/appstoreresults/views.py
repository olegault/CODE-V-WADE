from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import sqlite3
from django.template import loader


def index(request):

    try:
        sqliteConnection = sqlite3.connect('apptable.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")


        args=[]
        app_list =[]
        icon_list =[]
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

