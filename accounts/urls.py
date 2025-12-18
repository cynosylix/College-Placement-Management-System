from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("portal/", views.portal, name="portal"),
    path("register/student/", views.register_student, name="register_student"),
    path("register/tpo/", views.register_tpo, name="register_tpo"),
    path("register/recruiter/", views.register_recruiter, name="register_recruiter"),
]


