from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import RecruiterRegistrationForm, StudentRegistrationForm, TpoRegistrationForm
from .models import Profile


@login_required
def home(request):
    role = getattr(getattr(request.user, "profile", None), "role", None)
    if role == Profile.Role.STUDENT:
        return redirect("student:dashboard")
    if role == Profile.Role.TPO:
        return redirect("tpo:dashboard")
    if role == Profile.Role.RECRUITER:
        return redirect("recruiter:dashboard")
    return render(request, "home.html")


def portal(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "accounts/portal.html")


def register_student(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("home")
        messages.error(request, "Please correct the errors below.")
    else:
        form = StudentRegistrationForm()

    return render(request, "accounts/register.html", {"form": form, "role_label": "Student"})


def register_tpo(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = TpoRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your TPO account has been created.")
            return redirect("home")
        messages.error(request, "Please correct the errors below.")
    else:
        form = TpoRegistrationForm()

    return render(request, "accounts/register.html", {"form": form, "role_label": "TPO"})


def register_recruiter(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your recruiter account has been created.")
            return redirect("home")
        messages.error(request, "Please correct the errors below.")
    else:
        form = RecruiterRegistrationForm()

    return render(request, "accounts/register.html", {"form": form, "role_label": "Recruiter"})
