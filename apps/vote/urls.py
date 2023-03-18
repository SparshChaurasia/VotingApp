from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("<str:event_name>", views.event)
]
