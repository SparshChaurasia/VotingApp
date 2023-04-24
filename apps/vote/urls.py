from django.urls import path

from .views import index, vote, submit, get_student_details

urlpatterns = [
    path("", index),
    path("qvSeqpptuKuVyRONEqTJ", submit, name="submit"),
    path("EOIugodNIvWJOOamwUqw", get_student_details, name="get_student_details"),
    path("<str:event_name>", vote)
]
