from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render

from apps.vote.models import Category, Event, Option, Student


@login_required(login_url="/login")
def results(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponse(
            """<h3 style="text-align: center;">403 Forbidden</h3>
            <h4 style="text-align: center;">Missing required permissions.</h4>"""
        )
        
    params = {}

    events = Event.objects.all()
    for event in events:
        params[event] = {}
        categorys = Category.objects.filter(Event=event)
        for category in categorys:
            options = Option.objects.filter(OpitonCategory=category)
            params[event].update({category: options})
    return render(request, "results/results.html", {"params":params})


@login_required(login_url="/login")
def event_result(request, event_name):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponse(
            """<h3 style="text-align: center;">403 Forbidden</h3>
            <h4 style="text-align: center;">Missing required permissions.</h4>"""
        )    
    
    params = {}
    winners = {}

    event = Event.objects.get(EventName=event_name)
    categorys = Category.objects.filter(Event=event)
    for category in categorys:
        options = Option.objects.filter(OpitonCategory=category).order_by("-Votes")
        _w = options[0]
        w = [_w]
        for option in options:
            if option == _w:
                w.append(option)
                
        params.update({category: options})
        winners.update({category: w})

    
    return render(request, "results/event_result.html", {"params":params, "winners": winners, "event": event})
