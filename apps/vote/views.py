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
        # TODO: Send error notification to the client using Django messaging framework
        return HttpResponse("Already Voted")


    for category in categories:
        option_id = request.POST.get(category.CategoryName)
        option = Option.objects.get(OptionID=option_id)
        option.vote()
    
    student.voted(event_id)

    return HttpResponse("OK")



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
