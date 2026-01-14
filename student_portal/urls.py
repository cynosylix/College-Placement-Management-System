from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    
    # Profile Management
    path("profile/", views.profile_view, name="profile"),
    path("skill/add/", views.skill_add, name="skill_add"),
    path("skill/<int:pk>/delete/", views.skill_delete, name="skill_delete"),
    path("certification/add/", views.certification_add, name="certification_add"),
    path("certification/<int:pk>/delete/", views.certification_delete, name="certification_delete"),
    
    # Resume Builder
    path("resumes/", views.resume_list, name="resume_list"),
    path("resumes/create/", views.resume_create, name="resume_create"),
    path("resumes/<int:pk>/edit/", views.resume_edit, name="resume_edit"),
    path("resumes/<int:pk>/delete/", views.resume_delete, name="resume_delete"),
    
    # Portfolio
    path("portfolio/", views.portfolio_list, name="portfolio_list"),
    path("portfolio/add/", views.portfolio_add, name="portfolio_add"),
    path("portfolio/<int:pk>/delete/", views.portfolio_delete, name="portfolio_delete"),
    
    # Documents
    path("documents/", views.document_list, name="document_list"),
    path("documents/upload/", views.document_upload, name="document_upload"),
    path("documents/<int:pk>/delete/", views.document_delete, name="document_delete"),
    
    # Job Search & Applications
    path("jobs/", views.job_search, name="job_search"),
    path("jobs/<int:pk>/", views.job_detail, name="job_detail"),
    path("applications/", views.application_list, name="application_list"),
    path("applications/<int:pk>/", views.application_detail, name="application_detail"),
    path("saved-jobs/", views.saved_jobs, name="saved_jobs"),
    
    # Interviews
    path("interviews/", views.interview_list, name="interview_list"),
    
    # Messages
    path("messages/", views.message_list, name="message_list"),
    path("messages/send/", views.message_send, name="message_send"),
    
    # Notifications
    path("notifications/", views.notification_list, name="notification_list"),
    
    # Skill Development
    path("skill-gap-analysis/", views.skill_gap_analysis, name="skill_gap_analysis"),
    path("practice-tests/", views.practice_tests, name="practice_tests"),
    path("mock-interviews/", views.mock_interview_list, name="mock_interview_list"),
    path("mock-interviews/request/", views.mock_interview_request, name="mock_interview_request"),
]
