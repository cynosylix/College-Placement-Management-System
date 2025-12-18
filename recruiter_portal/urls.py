from django.urls import path

from . import views

app_name = "recruiter_portal"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]


