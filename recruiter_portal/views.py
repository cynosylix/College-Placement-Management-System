"""
Recruiter Portal: job postings CRUD, applications, interviews.
Role check: only users with Profile.role == RECRUITER.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from student_portal.models import JobPosting, Application, Interview

from .forms import ApplicationStatusForm, InterviewScheduleForm, JobPostingForm


def _recruiter_required(view_func):
    """Decorator: redirect to 403 if user is not a recruiter."""
    def wrapper(request: HttpRequest, *args, **kwargs):
        if getattr(getattr(request.user, "profile", None), "role", None) != Profile.Role.RECRUITER:
            return render(request, "errors/403.html", status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@_recruiter_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Dashboard with real stats for recruiter's jobs and applications."""
    jobs = JobPosting.objects.filter(posted_by=request.user)
    job_ids = list(jobs.values_list("id", flat=True))
    applications = Application.objects.filter(job_id__in=job_ids) if job_ids else Application.objects.none()

    stats = {
        "total_jobs": jobs.count(),
        "active_jobs": jobs.filter(is_active=True).count(),
        "total_applications": applications.count(),
        "shortlisted": applications.filter(status="shortlisted").count(),
        "interviews_scheduled": Interview.objects.filter(application__job__posted_by=request.user, status="scheduled").count(),
    }

    recent_applications = applications.select_related("student__user", "job").order_by("-applied_at")[:5]
    recent_jobs = jobs.order_by("-posted_at")[:5]

    context = {
        "stats": stats,
        "recent_applications": recent_applications,
        "recent_jobs": recent_jobs,
    }
    return render(request, "recruiter_portal/dashboard.html", context)


@login_required
@_recruiter_required
def job_list(request: HttpRequest) -> HttpResponse:
    """List recruiter's job postings with search and pagination."""
    from django.db.models import Q

    qs = JobPosting.objects.filter(posted_by=request.user).order_by("-posted_at")
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(company_name__icontains=search))

    paginator = Paginator(qs, 15)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "recruiter_portal/job_list.html", {"page_obj": page_obj, "search": search})


@login_required
@_recruiter_required
def job_create(request: HttpRequest) -> HttpResponse:
    """Create a new job posting."""
    if request.method == "POST":
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posting created successfully.")
            return redirect("recruiter:job_detail", pk=job.pk)
        messages.error(request, "Please correct the errors below.")
    else:
        form = JobPostingForm()
    return render(request, "recruiter_portal/job_form.html", {"form": form, "title": "Create Job Posting"})


@login_required
@_recruiter_required
def job_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """View job posting and link to applications."""
    job = get_object_or_404(JobPosting, pk=pk, posted_by=request.user)
    application_count = Application.objects.filter(job=job).count()
    shortlisted_count = Application.objects.filter(job=job, status="shortlisted").count()
    context = {
        "job": job,
        "application_count": application_count,
        "shortlisted_count": shortlisted_count,
    }
    return render(request, "recruiter_portal/job_detail.html", context)


@login_required
@_recruiter_required
def job_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Edit job posting."""
    job = get_object_or_404(JobPosting, pk=pk, posted_by=request.user)
    if request.method == "POST":
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job posting updated.")
            return redirect("recruiter:job_detail", pk=pk)
        messages.error(request, "Please correct the errors below.")
    else:
        form = JobPostingForm(instance=job)
    return render(request, "recruiter_portal/job_form.html", {"form": form, "job": job, "title": "Edit Job Posting"})


@login_required
@_recruiter_required
def job_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Deactivate or delete job posting."""
    job = get_object_or_404(JobPosting, pk=pk, posted_by=request.user)
    if request.method == "POST":
        job.is_active = False
        job.save()
        messages.success(request, "Job posting has been deactivated.")
        return redirect("recruiter:job_list")
    return render(request, "recruiter_portal/job_confirm_delete.html", {"job": job})


@login_required
@_recruiter_required
def application_list(request: HttpRequest, job_pk: int) -> HttpResponse:
    """List applications for a job with status filter."""
    job = get_object_or_404(JobPosting, pk=job_pk, posted_by=request.user)
    applications = Application.objects.filter(job=job).select_related("student__user", "resume").order_by("-applied_at")
    status_filter = request.GET.get("status")
    if status_filter:
        applications = applications.filter(status=status_filter)
    paginator = Paginator(applications, 15)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "job": job,
        "page_obj": page_obj,
        "status_filter": status_filter,
    }
    return render(request, "recruiter_portal/application_list.html", context)


@login_required
@_recruiter_required
def application_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """View application and update status / schedule interview."""
    application = get_object_or_404(Application, pk=pk, job__posted_by=request.user)
    interview = getattr(application, "interview", None)

    if request.method == "POST":
        if "update_status" in request.POST:
            form = ApplicationStatusForm(request.POST, instance=application)
            if form.is_valid():
                form.save()
                messages.success(request, "Application status updated.")
                return redirect("recruiter:application_detail", pk=pk)
        elif "schedule_interview" in request.POST and interview:
            form = InterviewScheduleForm(request.POST, instance=interview)
            if form.is_valid():
                form.save()
                messages.success(request, "Interview updated.")
                return redirect("recruiter:application_detail", pk=pk)
        elif "schedule_interview" in request.POST and not interview:
            form = InterviewScheduleForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.application = application
                obj.save()
                application.status = "interview_scheduled"
                application.save(update_fields=["status"])
                messages.success(request, "Interview scheduled.")
                return redirect("recruiter:application_detail", pk=pk)
    else:
        form = ApplicationStatusForm(instance=application)
        interview_form = InterviewScheduleForm(instance=interview) if interview else InterviewScheduleForm()

    context = {
        "application": application,
        "interview": interview,
        "form": form,
        "interview_form": interview_form,
    }
    return render(request, "recruiter_portal/application_detail.html", context)


@login_required
@_recruiter_required
def schedule_interview(request: HttpRequest, pk: int) -> HttpResponse:
    """Standalone page to schedule interview for an application."""
    application = get_object_or_404(Application, pk=pk, job__posted_by=request.user)
    interview, created = Interview.objects.get_or_create(application=application, defaults={"status": "scheduled"})
    if request.method == "POST":
        form = InterviewScheduleForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            application.status = "interview_scheduled"
            application.save(update_fields=["status"])
            messages.success(request, "Interview scheduled.")
            return redirect("recruiter:application_detail", pk=pk)
    else:
        form = InterviewScheduleForm(instance=interview)
    return render(request, "recruiter_portal/schedule_interview.html", {"form": form, "application": application})
