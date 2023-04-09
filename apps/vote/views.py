from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse

from .models import Event, Student, Option, Category


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
    categories = Category.objects.filter(Event=event)

    if s_id:
        student = Student.objects.get(StudentID=s_id)
    else:
        student = Student.objects.filter(Class=s_class).get(Name=s_name)
    
    if student.has_voted(event_id):
        # TODO: Send error notification to the frontend using Django messaging framework.
        return HttpResponse("Already Voted")


    for category in categories:
        option_id = request.POST.get(category.CategoryName)
        option = Option.objects.get(OptionID=option_id)
        option.vote()
    
    student.voted(event_id)
    
    # TODO: Send success notification to the frontend using Django messaging framework.
    return HttpResponse("OK")



@login_required(login_url="/login")
def results(request):
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
