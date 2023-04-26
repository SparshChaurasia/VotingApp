from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

from apps.vote import models as v_models

from .models import Category, Event, Option, Student


@csrf_exempt
def get_student_details(request):
    if request.method != "POST":
        return HttpResponse(
            """<h3 style="text-align: center;">403 Forbidden</h3>
            <h4 style="text-align: center;">Invalid request method</h4>"""
        ) 

    s_id = request.POST.get("id").upper()
    s_name = request.POST.get("name").upper()
    s_class = request.POST.get("class")

    try:
        if s_id:
            student = Student.objects.get(StudentID=s_id)
        else:
            student = Student.objects.filter(Class=s_class).get(Name=s_name)

    except v_models.Student.DoesNotExist:
        return JsonResponse({"Status": 404})

    
    # _events = eval(student.Voted).keys()
    res = {
        "Status": 200,
        "StudentID": student.StudentID,
        "Name": student.Name,
        "Class": student.Class,
        # "Voted": _events
    }
    return JsonResponse(res)

@login_required(login_url="/login")
def index(request):
    if request.user.is_staff and not request.user.is_superuser:
        return HttpResponse(
            """<h3 style="text-align: center;">403 Forbidden</h3>
            <h4 style="text-align: center;">Only class teachers have access to voting page.</h4>"""
        )
    events = Event.objects.all()

    params = {
        "events": events
    }
    return render(request, "vote/vote.html", params)    

@login_required(login_url="/login")
def vote(request, event_name):
    if request.user.is_staff and not request.user.is_superuser:
        return HttpResponse(
            """<h3 style="text-align: center;">403 Forbidden</h3>
            <h4 style="text-align: center;">Only class teachers have access to voting page.</h4>"""
        )
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

    s_id = request.POST.get("s_id").upper()
    s_name = request.POST.get("name").upper()
    s_class = request.POST.get("class")

    event_id = int(request.POST.get("event_id"))
    event = Event.objects.get(EventID=event_id)
    event_name = event.EventName
    categories = Category.objects.filter(Event=event)

    if not s_id or all([s_name, s_class]):
        messages.warning(request, "Invalid student details.")
        return redirect(f"/vote/{event_name}")

    try:
        if s_id:
            student = Student.objects.get(StudentID=s_id)
        else:
            student = Student.objects.filter(Class=s_class).get(Name=s_name)
    except v_models.Student.DoesNotExist:
        messages.warning(request, "Student not found.")
        return redirect(f"/vote/{event_name}")

    if student.has_voted(event_id):
        messages.warning(request, "Student has already voted once.")
        return redirect(f"/vote/{event_name}")

    options = [] # List of candidates voted
    for category in categories:
        option_id = request.POST.get(category.CategoryName)
        option = Option.objects.get(OptionID=option_id)
        options.append(option)
        option.vote()
    
    student.voted(event_id, options)
    
    messages.success(request, "Successfully voted.")
    return redirect(f"/vote/{event_name}")
