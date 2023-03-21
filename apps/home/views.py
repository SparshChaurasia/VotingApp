from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/login")
def index(request):
    return render(request, "index.html")


@login_required(login_url="/login")
def event(request, event_name):
    event_pages = {
        # event_name: event_page
    }
    event_page = event_pages.get(event_name, "events/event.html") # default event page

    return render(request, event_page)