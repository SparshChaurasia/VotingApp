from django.urls import path

from .views import index, vote

urlpatterns = [
    path("", index),
    path("<str:event_name>", vote)
]
