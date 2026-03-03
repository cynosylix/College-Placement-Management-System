from django.urls import path

from . import views

app_name = "tpo"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("students/", views.student_list, name="student_list"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("applications/", views.application_list, name="application_list"),
    path("applications/<int:pk>/", views.application_detail, name="application_detail"),
    path("jobs/", views.job_list, name="job_list"),
    path("reports/", views.reports, name="reports"),
    path("reports/placement-pdf/", views.report_placement_pdf, name="report_placement_pdf"),
]
