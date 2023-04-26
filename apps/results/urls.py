from django.urls import path
from .views import results, event_result, get_candidate_report, get_class_report

urlpatterns = [
    path("", results),
    path("rAFoMAdlLxmlmUniJqVR", get_candidate_report, name="get_candidate_report"),
    path("oEwJrqZNweOGWpdTAAQK", get_class_report, name="get_class_report"),
    path("<str:event_name>", event_result) 
]
