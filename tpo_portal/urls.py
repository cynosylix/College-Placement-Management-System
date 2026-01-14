from django.urls import path

from . import views

app_name = "tpo"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]


