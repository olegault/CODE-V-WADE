from django.shortcuts import render


def index(request):
    return render(request, "index.html")

def alphademo(request):
    return render(request, "alphademo.html")

def about(request):
    return render(request, "about.html")

def scorecard(request):
    return render(request, "scorecard.html")

def contact(request):
    return render(request, "contact.html")

