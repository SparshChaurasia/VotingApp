import csv
import os
from datetime import datetime
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

from apps.vote.models import Category, Event, Option, Student

BASE_DIR = Path(__file__).resolve().parent


def get_candidate_report(request):
    if request.method != "POST":
        return HttpResponse(
            """<h3 style="text-align: center;">403 Forbidden</h3>
            <h4 style="text-align: center;">Invalid request method.</h4>"""
        ) 
    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    event_id = request.POST.get("event_id")
    options = Option.objects.filter(OptionEvent=event_id)

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="candidate_report_{timestamp}.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["OptionID", "OpitonCategory", "OptionName", "Votes"])
    for option in options:
        writer.writerow([option.OptionID, option.OpitonCategory, option.OptionName, option.Votes])

    return response


def get_class_report(request):
    if request.method != "POST":
        return HttpResponse(
            """<h3 style="text-align: center;">403 Forbidden</h3>
            <h4 style="text-align: center;">Invalid request method.</h4>"""
        ) 

    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    s_class = request.POST.get("class")
    event_id = request.POST.get("event_id")
    students = Student.objects.filter(Class=s_class)
    

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="class_{s_class}_report_{timestamp}.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["StudentID", "Name", "Class", "Voted"])
    for student in students:
        writer.writerow([student.StudentID, student.Name, student.Class, student.has_voted(event_id)])

    return response


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
