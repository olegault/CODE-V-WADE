from django.contrib import admin
from django.urls import path
from django.urls import include
from appstoreresults import views
from django.http import HttpResponse
from .views import index

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('scorecard', views.scorecard, name='scorecard'),
    path('scorecard/<str:appID>', views.scorecard, name='scorecard'),
    path('submit', views.submit, name='submit'),
    path('submitdone', views.submitdone, name='submit'),
    path('PageObjects', views.PageObjects, name='PageObjects'),
    
    #location paths
    path('northamerica', views.northamerica, name='northamerica'),
    path('southamerica', views.southamerica, name='southamerica'),
    path('europe', views.europe, name='europe'),
    path('africa', views.africa, name='africa'),
    path('australia', views.australia, name='australia'),
    path('asia', views.asia, name='asia'),
]
