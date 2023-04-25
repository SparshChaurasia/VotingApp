from django.urls import path
from .views import results, event_result

urlpatterns = [
    path("", results),
    path("<str:event_name>", event_result) 
]
