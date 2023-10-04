"""
VotingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

import apps.home.views as home_views
# from apps.home.views import index, event, dashboard

admin.site.site_header  =  "Voting App Administration"  
admin.site.site_title  =  "Voting App Administration"
admin.site.index_title  =  "Site Administration"

urlpatterns = [
    path("login/", include("apps.login.urls")),
    path("", home_views.index),
    path("dashboard/", home_views.dashboard),
    # path("<str:event_name>", event),
    path("vote/", include("apps.vote.urls")),
    path("results/", include("apps.results.urls")),
    path("admin/", admin.site.urls)
]
