from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.vote.models import Event, Student, Option, Category



@login_required(login_url="/login")
def index(request):
    return render(request, "index.html")


# @login_required(login_url="/login")
# def event(request, event_name):
#     event_pages = {
#         # event_name: event_page
#     }
#     event_page = event_pages.get(event_name, "events/event.html") # default event page

#     return render(request, event_page)


@login_required(login_url="/login")
def dashboard(request):
    # s_class = None
    # s_total = None
    # s_voted = None
    # s_not_voted = None

    # if request.method == "POST":
    #     s_class = request.POST.get("class")
    #     students = Student.objects.filter(Class=s_class)

    #     s_total = students.count()
    #     s_voted = students.filter(Voted=True).count()
    #     s_not_voted = students.filter(Voted=False).count()

    # events = Event.objects.all()
    # params = {
    #     "events": events,
        # "class": s_class, 
        # "total": s_total,
        # "voted": s_voted, 
        # "not_voted": s_not_voted
    # }
    params = {}
    # students = Student.objects.all()
    
    events = Event.objects.all()
    for event in events:
        params[event] = {}
        categorys = Category.objects.filter(Event=event)
        for category in categorys:
            options = Option.objects.filter(OpitonCategory=category)
            params[event].update({category: options})
    return render(request, "dashboard.html", {"params":params})
