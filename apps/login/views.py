from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, redirect, render

from .decorators import unauthenticated_user


@unauthenticated_user
def index(request):
    return render(request, "login.html")

def login_user(request):
    if request.method != "POST":
        return HttpResponse("Bad request method")
    
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)
    if not user:
        messages.error(request, "User not found")
        return redirect("/login")

    login(request, user)
    return redirect("/")

def logout_user(request):
    logout(request)
   
    return redirect("/login")

