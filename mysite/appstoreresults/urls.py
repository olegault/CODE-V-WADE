from django.contrib import admin
from django.urls import path
from django.urls import include
from appstoreresults import views
from .views import index

urlpatterns = [
    path('', views.index, name='index'),
    path('alphademo', views.alphademo, name='alphademo'),
    path('about', views.about, name='about'),
    path('scorecard', views.scorecard, name='scorecard'),
    path('contact', views.contact, name='contact'),
]
