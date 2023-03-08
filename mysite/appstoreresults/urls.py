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
]
