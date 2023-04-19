from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render, redirect

from apps.vote import models as v_models
from .models import Category, Event, Option, Student


@login_required(login_url="/login")
def index(request):
    events = Event.objects.all()

    params = {
        "events": events
    }
    return render(request, "vote/vote.html", params)    

@login_required(login_url="/login")
def vote(request, event_name):
    event = Event.objects.get(EventName=event_name)
    categorys = Category.objects.filter(Event=event)
    options = Option.objects.filter(OptionEvent=event)
    
    params = {
        "event": event,
        "categorys": categorys,
        "options": options
    }
    return render(request, "vote/form.html", params)

@login_required(login_url="/login")
def submit(request):
    if request.method != "POST":
        return HttpResponse(
            """<h3 style="text-align: center;">403 Forbidden</h3>
            <h4 style="text-align: center;">Invalid request method</h4>"""
        )

    s_id = request.POST.get("s_id")
    s_name = request.POST.get("name").upper()
    s_class = request.POST.get("class")

    event_id = int(request.POST.get("event_id"))
    event = Event.objects.get(EventID=event_id)
    event_name = event.EventName
    categories = Category.objects.filter(Event=event)

    if not s_id or all([s_name, s_class]):
        messages.warning(request, "Invalid student details.")
        return redirect(f"/vote/{event_name}")

    if s_id:
        try:
            student = Student.objects.get(StudentID=s_id)
        except v_models.Student.DoesNotExist:
            messages.warning(request, "Student not found.")
            return redirect(f"/vote/{event_name}")
    else:
        student = Student.objects.filter(Class=s_class).get(Name=s_name)
        if not student:
            messages.warning(request, "Student not found.")
            return redirect(f"/vote/{event_name}")

    if student.has_voted(event_id):
        messages.warning(request, "Student has already voted once.")
        return redirect(f"/vote/{event_name}")

    for category in categories:
        option_id = request.POST.get(category.CategoryName)
        option = Option.objects.get(OptionID=option_id)
        option.vote()
    
    student.voted(event_id)
    
    messages.success(request, "Successfully voted.")
    return redirect(f"/vote/{event_name}")



@login_required(login_url="/login")
def results(request):
    if not request.user.is_superuser:
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
    if not request.user.is_superuser:
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
        w = options[0]
        params.update({category: options})
        winners.update({category: w})

    
    return render(request, "results/event_result.html", {"params":params, "winners": winners, "event": event})
