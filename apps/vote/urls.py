from django.urls import path

from .views import *

urlpatterns = [
    path("", index),
    path("EOIugodNIvWJOOamwUqw", get_student_details, name="get_student_details"),
    # path("<str:category>/", category_index),
    path("student/", lambda request: category_index(request, category="student")),
    path("staff/", lambda request: category_index(request, category="staff")),
    path("visitor/", lambda request: category_index(request, category="visitor")),
    path("student/<str:event_name>", lambda request, event_name: vote(request, category="student", event_name=event_name)),
    path("staff/<str:event_name>", lambda request, event_name: vote(request, category="staff", event_name=event_name)),
    path("visitor/<str:event_name>", lambda request, event_name: vote(request, category="visitor", event_name=event_name)),
    
    path("qvSeqpptuKuVyRONEqTJ", submit, name="submit"),
    # path("visitors_vote/yDlPCCCymLZMKAMWNiQk", visitors_submit),
    path("staff_vote/uwfbAKykNtbryLMXAXuV", staff_submit, name="staff_submit"),
]
