from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from accounts.models import Profile


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    if getattr(getattr(request.user, "profile", None), "role", None) != Profile.Role.RECRUITER:
        return render(request, "errors/403.html", status=403)
    return render(request, "recruiter_portal/dashboard.html")
