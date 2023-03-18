from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Event, Student, Option, Category


@login_required(login_url="/login")
def index(request):
    events = Event.objects.all()
    params = {
        "events": events,
    }
    return render(request, "vote.html", params)

@login_required(login_url="/login")
def event(request, event_name):
    event_pages = { # custom event pages
        # event_name: event_page
    }
    event_page = event_pages.get(event_name, "events/event.html") # default event page

    event = Event.objects.get(EventName=event_name)
    categorys = Category.objects.filter(Event=event)
    options = Option.objects.filter(OptionEvent=event)

    params = {
        "event_name": event_name,
        "categorys": categorys,
        "options": options
    }
    return render(request, event_page, params)

@login_required(login_url="/login")
def results(request):
    return render(request, "results.html")

@login_required(login_url="/login")
def dashboard(request):
    s_class = None
    s_total = None
    s_voted = None
    s_not_voted = None

    if request.method == "POST":
        s_class = request.POST.get("class")
        students = Student.objects.filter(Class=s_class)

        s_total = students.count()
        s_voted = students.filter(Voted=True).count()
        s_not_voted = students.filter(Voted=False).count()

    events = Event.objects.all()
    params = {
        "events": events,
        "class": s_class, 
        "total": s_total,
        "voted": s_voted, 
        "not_voted": s_not_voted
    }

    return render(request, "dashboard.html", params)
