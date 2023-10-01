from django.shortcuts import redirect, HttpResponse

def unauthenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        return func(request, *args, **kwargs)
    
    return wrapper