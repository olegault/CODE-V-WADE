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
    path('writing4', views.writing4, name='writing4'),
    path('scorecard', views.scorecard, name='scorecard'),
]
