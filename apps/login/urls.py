from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("RWXddGRprEsVxTaltGzt", views.login_user, name="login"),
    path("xbriVVkFqxxMQLwouLXq", views.logout_user, name="logout")
]