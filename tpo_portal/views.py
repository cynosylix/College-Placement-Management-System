"""
TPO Portal: student management, application review, placement workflow.
Only users with Profile.role == TPO can access.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from student_portal.models import (
    StudentProfile,
    JobPosting,
    Application,
    Interview,
)

from .forms import ApplicationStatusForm, InterviewScheduleForm, StudentEligibilityForm


def _tpo_required(view_func):
    """Decorator: 403 if user is not TPO."""
    def wrapper(request: HttpRequest, *args, **kwargs):
        if getattr(getattr(request.user, "profile", None), "role", None) != Profile.Role.TPO:
            return render(request, "errors/403.html", status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@_tpo_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Dashboard with real stats: students, recruiters, jobs, applications."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    total_students = StudentProfile.objects.count()
    eligible_students = StudentProfile.objects.filter(placement_eligible=True).count()
    recruiters = User.objects.filter(profile__role=Profile.Role.RECRUITER).count()
    jobs = JobPosting.objects.filter(is_active=True).count()
    applications = Application.objects.count()
    shortlisted = Application.objects.filter(status="shortlisted").count()
    interviews = Interview.objects.filter(status="scheduled").count()

    stats = {
        "total_students": total_students,
        "eligible_students": eligible_students,
        "recruiters": recruiters,
        "jobs": jobs,
        "applications": applications,
        "shortlisted": shortlisted,
        "interviews": interviews,
    }

    recent_applications = Application.objects.select_related(
        "student__user", "job"
    ).order_by("-applied_at")[:10]

    context = {"stats": stats, "recent_applications": recent_applications}
    return render(request, "tpo_portal/dashboard.html", context)


@login_required
@_tpo_required
def student_list(request: HttpRequest) -> HttpResponse:
    """List all students with search and filter by branch/course/eligibility."""
    qs = StudentProfile.objects.select_related("user").order_by("user__username")
    search = request.GET.get("search", "").strip()
    branch = request.GET.get("branch", "").strip()
    course = request.GET.get("course", "").strip()
    eligible = request.GET.get("eligible", "").strip()

    if search:
        qs = qs.filter(
            Q(user__username__icontains=search)
            | Q(user__email__icontains=search)
            | Q(enrollment_number__icontains=search)
        )
    if branch:
        qs = qs.filter(branch__iexact=branch)
    if course:
        qs = qs.filter(course__iexact=course)
    if eligible == "1":
        qs = qs.filter(placement_eligible=True)
    elif eligible == "0":
        qs = qs.filter(placement_eligible=False)

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    # Distinct branches/courses for filter dropdowns
    branches = StudentProfile.objects.exclude(branch="").values_list("branch", flat=True).distinct()
    courses = StudentProfile.objects.exclude(course="").values_list("course", flat=True).distinct()

    context = {
        "page_obj": page_obj,
        "search": search,
        "branch": branch,
        "course": course,
        "eligible": eligible,
        "branches": branches,
        "courses": courses,
    }
    return render(request, "tpo_portal/student_list.html", context)


@login_required
@_tpo_required
def student_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """View student and toggle placement eligibility."""
    student = get_object_or_404(StudentProfile, pk=pk)
    if request.method == "POST":
        form = StudentEligibilityForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Eligibility updated.")
            return redirect("tpo:student_detail", pk=pk)
    else:
        form = StudentEligibilityForm(instance=student)

    applications = Application.objects.filter(student=student).select_related("job").order_by("-applied_at")[:10]
    context = {"student": student, "form": form, "applications": applications}
    return render(request, "tpo_portal/student_detail.html", context)


@login_required
@_tpo_required
def application_list(request: HttpRequest) -> HttpResponse:
    """List all applications with status filter and pagination."""
    qs = Application.objects.select_related("student__user", "job").order_by("-applied_at")
    status_filter = request.GET.get("status")
    if status_filter:
        qs = qs.filter(status=status_filter)
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"page_obj": page_obj, "status_filter": status_filter}
    return render(request, "tpo_portal/application_list.html", context)


@login_required
@_tpo_required
def application_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """View application and update status / schedule interview (TPO can do for any application)."""
    application = get_object_or_404(Application, pk=pk)
    interview = getattr(application, "interview", None)

    if request.method == "POST":
        if "update_status" in request.POST:
            form = ApplicationStatusForm(request.POST, instance=application)
            if form.is_valid():
                form.save()
                messages.success(request, "Application status updated.")
                return redirect("tpo:application_detail", pk=pk)
        elif "schedule_interview" in request.POST:
            if interview:
                form = InterviewScheduleForm(request.POST, instance=interview)
                if form.is_valid():
                    form.save()
                    application.status = "interview_scheduled"
                    application.save(update_fields=["status"])
                    messages.success(request, "Interview updated.")
                    return redirect("tpo:application_detail", pk=pk)
            else:
                form = InterviewScheduleForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.application = application
                    obj.save()
                    application.status = "interview_scheduled"
                    application.save(update_fields=["status"])
                    messages.success(request, "Interview scheduled.")
                    return redirect("tpo:application_detail", pk=pk)
    else:
        form = ApplicationStatusForm(instance=application)
        interview_form = InterviewScheduleForm(instance=interview) if interview else InterviewScheduleForm()

    context = {
        "application": application,
        "interview": interview,
        "form": form,
        "interview_form": interview_form,
    }
    return render(request, "tpo_portal/application_detail.html", context)


@login_required
@_tpo_required
def job_list(request: HttpRequest) -> HttpResponse:
    """List all job postings (read-only for TPO)."""
    qs = JobPosting.objects.select_related("posted_by").filter(is_active=True).order_by("-posted_at")
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(
            Q(title__icontains=search) | Q(company_name__icontains=search)
        )
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"page_obj": page_obj, "search": search}
    return render(request, "tpo_portal/job_list.html", context)


@login_required
@_tpo_required
def reports(request: HttpRequest) -> HttpResponse:
    """Reports and analytics dashboard."""
    from django.db.models import Count

    total_students = StudentProfile.objects.count()
    eligible = StudentProfile.objects.filter(placement_eligible=True).count()
    total_applications = Application.objects.count()
    placed = Application.objects.filter(status="accepted").count()
    shortlisted = Application.objects.filter(status="shortlisted").count()
    rejected = Application.objects.filter(status="rejected").count()

    # Department-wise: students and applications
    dept_students = (
        StudentProfile.objects.exclude(branch="")
        .values("branch")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    dept_applications = (
        Application.objects.filter(student__branch__isnull=False)
        .exclude(student__branch="")
        .values("student__branch")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    dept_applications = [{"branch": x["student__branch"], "count": x["count"]} for x in dept_applications]

    # Status breakdown
    status_breakdown = (
        Application.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    context = {
        "total_students": total_students,
        "eligible": eligible,
        "total_applications": total_applications,
        "placed": placed,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "dept_students": dept_students,
        "dept_applications": dept_applications,
        "status_breakdown": status_breakdown,
    }
    return render(request, "tpo_portal/reports.html", context)


@login_required
@_tpo_required
def report_placement_pdf(request: HttpRequest) -> HttpResponse:
    """Placement report as HTML for print/PDF (Save as PDF from browser)."""
    from django.db.models import Count
    from django.utils import timezone

    now = timezone.now()
    total_students = StudentProfile.objects.count()
    eligible = StudentProfile.objects.filter(placement_eligible=True).count()
    total_applications = Application.objects.count()
    placed = Application.objects.filter(status="accepted").count()
    dept_students = (
        StudentProfile.objects.exclude(branch="")
        .values("branch")
        .annotate(count=Count("id"))
        .order_by("branch")
    )
    status_breakdown = (
        Application.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )

    context = {
        "now": now,
        "total_students": total_students,
        "eligible": eligible,
        "total_applications": total_applications,
        "placed": placed,
        "dept_students": dept_students,
        "status_breakdown": status_breakdown,
    }
    return render(request, "tpo_portal/report_placement_pdf.html", context)
