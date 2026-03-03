from django.urls import path

from . import views

app_name = "recruiter"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/create/", views.job_create, name="job_create"),
    path("jobs/<int:pk>/", views.job_detail, name="job_detail"),
    path("jobs/<int:pk>/edit/", views.job_edit, name="job_edit"),
    path("jobs/<int:pk>/delete/", views.job_delete, name="job_delete"),
    path("jobs/<int:job_pk>/applications/", views.application_list, name="application_list"),
    path("applications/<int:pk>/", views.application_detail, name="application_detail"),
    path("applications/<int:pk>/schedule-interview/", views.schedule_interview, name="schedule_interview"),
]
