from django.urls import path

from .views import index, vote, submit

urlpatterns = [
    path("", index),
    path("qvSeqpptuKuVyRONEqTJ", submit, name="submit"),
    path("<str:event_name>", vote)
]
