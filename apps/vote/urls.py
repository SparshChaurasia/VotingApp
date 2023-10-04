from django.urls import path

from .views import *

urlpatterns = [
    path("", index),
    path("EOIugodNIvWJOOamwUqw", get_student_details, name="get_student_details"),
    path("qvSeqpptuKuVyRONEqTJ", submit, name="submit"),
    path("uwfbAKykNtbryLMXAXuV", staff_submit, name="staff_submit"),
    path("odNIvWptktbrEOIuuKuV", visitor_submit, name="visitor_submit"),
    path("<str:category>/", category_index),
    path("<str:category>/<str:event_name>", vote),
    
]
