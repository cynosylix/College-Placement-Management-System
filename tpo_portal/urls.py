from django.urls import path

from . import views

app_name = "tpo_portal"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]


