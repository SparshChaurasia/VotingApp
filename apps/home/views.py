from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.login.decorators import unauthenticated_user

from apps.vote.models import Category, Event, Option, Student


@unauthenticated_user
def index(request):
    return render(request, "index.html")


@login_required(login_url="/login")
def dashboard(request):
    params = {}
    
    events = Event.objects.all()
    for event in events:
        params[event] = {}
        categorys = Category.objects.filter(Event=event)
        for category in categorys:
            options = Option.objects.filter(OpitonCategory=category)
            params[event].update({category: options})
    return render(request, "dashboard.html", {"params":params})
