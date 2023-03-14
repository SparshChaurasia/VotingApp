from django.shortcuts import redirect, HttpResponse

def unauthenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return func(request, *args, **kwargs)
    
    return wrapper