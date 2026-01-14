from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone

from accounts.models import Profile
from .models import (
    StudentProfile, Skill, Certification, Resume, PortfolioItem,
    Document, JobPosting, Application, SavedJob, Interview,
    Message, Notification, SkillGapAnalysis, PracticeTest, MockInterview
)
from .forms import (
    StudentProfileForm, SkillForm, CertificationForm, ResumeForm,
    PortfolioItemForm, DocumentForm, ApplicationForm, MessageForm,
    MockInterviewForm, JobSearchForm
)


def get_student_profile(user):
    """Helper to get or create student profile"""
    profile, created = StudentProfile.objects.get_or_create(user=user)
    return profile


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Enhanced dashboard with stats"""
    if getattr(getattr(request.user, "profile", None), "role", None) != Profile.Role.STUDENT:
        return render(request, "errors/403.html", status=403)
    
    student = get_student_profile(request.user)
    
    # Statistics
    stats = {
        'total_applications': Application.objects.filter(student=student).count(),
        'shortlisted': Application.objects.filter(student=student, status='shortlisted').count(),
        'pending': Application.objects.filter(student=student, status__in=['applied', 'under_review']).count(),
        'interviews': Interview.objects.filter(application__student=student, status='scheduled').count(),
        'saved_jobs': SavedJob.objects.filter(student=student).count(),
    }
    
    # Recent applications
    recent_applications = Application.objects.filter(student=student).select_related('job')[:5]
    
    # Upcoming interviews
    upcoming_interviews = Interview.objects.filter(
        application__student=student,
        status='scheduled',
        scheduled_at__gte=timezone.now()
    ).select_related('application__job')[:5]
    
    # Recent notifications
    recent_notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    
    context = {
        'student': student,
        'stats': stats,
        'recent_applications': recent_applications,
        'upcoming_interviews': upcoming_interviews,
        'recent_notifications': recent_notifications,
    }
    return render(request, "student_portal/dashboard.html", context)


# ========== PROFILE MANAGEMENT ==========

@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """View and edit student profile"""
    if getattr(getattr(request.user, "profile", None), "role", None) != Profile.Role.STUDENT:
        return render(request, "errors/403.html", status=403)
    
    student = get_student_profile(request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student:profile')
    else:
        form = StudentProfileForm(instance=student)
    
    context = {
        'student': student,
        'form': form,
        'skills': student.skills.all(),
        'certifications': student.certifications.all(),
    }
    return render(request, "student_portal/profile.html", context)


@login_required
def skill_add(request: HttpRequest) -> HttpResponse:
    """Add a skill"""
    if request.method == 'POST':
        student = get_student_profile(request.user)
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.student = student
            skill.save()
            messages.success(request, "Skill added successfully!")
            return redirect('student:profile')
    return redirect('student:profile')


@login_required
def skill_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a skill"""
    skill = get_object_or_404(Skill, pk=pk, student__user=request.user)
    skill.delete()
    messages.success(request, "Skill deleted!")
    return redirect('student:profile')


@login_required
def certification_add(request: HttpRequest) -> HttpResponse:
    """Add a certification"""
    if request.method == 'POST':
        student = get_student_profile(request.user)
        form = CertificationForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.student = student
            cert.save()
            messages.success(request, "Certification added successfully!")
            return redirect('student:profile')
    return redirect('student:profile')


@login_required
def certification_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a certification"""
    cert = get_object_or_404(Certification, pk=pk, student__user=request.user)
    cert.delete()
    messages.success(request, "Certification deleted!")
    return redirect('student:profile')


# ========== RESUME BUILDER ==========

@login_required
def resume_list(request: HttpRequest) -> HttpResponse:
    """List all resumes"""
    student = get_student_profile(request.user)
    resumes = Resume.objects.filter(student=student)
    return render(request, "student_portal/resume_list.html", {'resumes': resumes})


@login_required
def resume_create(request: HttpRequest) -> HttpResponse:
    """Create a new resume"""
    student = get_student_profile(request.user)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.student = student
            if resume.is_default:
                Resume.objects.filter(student=student).update(is_default=False)
            resume.save()
            messages.success(request, "Resume created successfully!")
            return redirect('student:resume_list')
    else:
        form = ResumeForm()
    
    return render(request, "student_portal/resume_form.html", {'form': form, 'title': 'Create Resume'})


@login_required
def resume_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Edit a resume"""
    resume = get_object_or_404(Resume, pk=pk, student__user=request.user)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            if form.cleaned_data['is_default']:
                Resume.objects.filter(student=resume.student).exclude(pk=pk).update(is_default=False)
            form.save()
            messages.success(request, "Resume updated successfully!")
            return redirect('student:resume_list')
    else:
        form = ResumeForm(instance=resume)
    
    return render(request, "student_portal/resume_form.html", {'form': form, 'resume': resume, 'title': 'Edit Resume'})


@login_required
def resume_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a resume"""
    resume = get_object_or_404(Resume, pk=pk, student__user=request.user)
    resume.delete()
    messages.success(request, "Resume deleted!")
    return redirect('student:resume_list')


# ========== PORTFOLIO ==========

@login_required
def portfolio_list(request: HttpRequest) -> HttpResponse:
    """List portfolio items"""
    student = get_student_profile(request.user)
    portfolio_items = PortfolioItem.objects.filter(student=student)
    return render(request, "student_portal/portfolio_list.html", {'portfolio_items': portfolio_items})


@login_required
def portfolio_add(request: HttpRequest) -> HttpResponse:
    """Add portfolio item"""
    student = get_student_profile(request.user)
    
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.student = student
            item.save()
            messages.success(request, "Portfolio item added successfully!")
            return redirect('student:portfolio_list')
    else:
        form = PortfolioItemForm()
    
    return render(request, "student_portal/portfolio_form.html", {'form': form, 'title': 'Add Portfolio Item'})


@login_required
def portfolio_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete portfolio item"""
    item = get_object_or_404(PortfolioItem, pk=pk, student__user=request.user)
    item.delete()
    messages.success(request, "Portfolio item deleted!")
    return redirect('student:portfolio_list')


# ========== DOCUMENTS ==========

@login_required
def document_list(request: HttpRequest) -> HttpResponse:
    """List documents"""
    student = get_student_profile(request.user)
    documents = Document.objects.filter(student=student)
    return render(request, "student_portal/document_list.html", {'documents': documents})


@login_required
def document_upload(request: HttpRequest) -> HttpResponse:
    """Upload a document"""
    student = get_student_profile(request.user)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.student = student
            doc.save()
            messages.success(request, "Document uploaded successfully!")
            return redirect('student:document_list')
    else:
        form = DocumentForm()
    
    return render(request, "student_portal/document_form.html", {'form': form})


@login_required
def document_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a document"""
    doc = get_object_or_404(Document, pk=pk, student__user=request.user)
    doc.delete()
    messages.success(request, "Document deleted!")
    return redirect('student:document_list')


# ========== JOB SEARCH & APPLICATIONS ==========

@login_required
def job_search(request: HttpRequest) -> HttpResponse:
    """Browse and search jobs"""
    student = get_student_profile(request.user)
    form = JobSearchForm(request.GET)
    
    jobs = JobPosting.objects.filter(is_active=True)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        job_type = form.cleaned_data.get('job_type')
        location = form.cleaned_data.get('location')
        
        if search:
            jobs = jobs.filter(
                Q(title__icontains=search) |
                Q(company_name__icontains=search) |
                Q(description__icontains=search)
            )
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if location:
            jobs = jobs.filter(location__icontains=location)
    
    # Get saved job IDs
    saved_job_ids = set(SavedJob.objects.filter(student=student).values_list('job_id', flat=True))
    
    # Get applied job IDs
    applied_job_ids = set(Application.objects.filter(student=student).values_list('job_id', flat=True))
    
    paginator = Paginator(jobs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'saved_job_ids': saved_job_ids,
        'applied_job_ids': applied_job_ids,
    }
    return render(request, "student_portal/job_search.html", context)


@login_required
def job_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """View job details"""
    job = get_object_or_404(JobPosting, pk=pk, is_active=True)
    student = get_student_profile(request.user)
    
    # Check if already applied
    application = Application.objects.filter(student=student, job=job).first()
    is_saved = SavedJob.objects.filter(student=student, job=job).exists()
    
    # Get available resumes
    resumes = Resume.objects.filter(student=student)
    
    if request.method == 'POST':
        if 'apply' in request.POST:
            if application:
                messages.warning(request, "You have already applied for this job.")
            else:
                app_form = ApplicationForm(request.POST)
                if app_form.is_valid():
                    app = app_form.save(commit=False)
                    app.student = student
                    app.job = job
                    app.save()
                    messages.success(request, "Application submitted successfully!")
                    return redirect('student:application_detail', pk=app.pk)
        elif 'save' in request.POST:
            SavedJob.objects.get_or_create(student=student, job=job)
            messages.success(request, "Job saved!")
            return redirect('student:job_detail', pk=pk)
        elif 'unsave' in request.POST:
            SavedJob.objects.filter(student=student, job=job).delete()
            messages.success(request, "Job removed from saved!")
            return redirect('student:job_detail', pk=pk)
    
    app_form = ApplicationForm(initial={'resume': resumes.filter(is_default=True).first()})
    
    context = {
        'job': job,
        'application': application,
        'is_saved': is_saved,
        'app_form': app_form,
        'resumes': resumes,
    }
    return render(request, "student_portal/job_detail.html", context)


@login_required
def application_list(request: HttpRequest) -> HttpResponse:
    """List all applications"""
    student = get_student_profile(request.user)
    applications = Application.objects.filter(student=student).select_related('job')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, "student_portal/application_list.html", context)


@login_required
def application_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """View application details"""
    application = get_object_or_404(Application, pk=pk, student__user=request.user)
    interview = getattr(application, 'interview', None)
    
    context = {
        'application': application,
        'interview': interview,
    }
    return render(request, "student_portal/application_detail.html", context)


@login_required
def saved_jobs(request: HttpRequest) -> HttpResponse:
    """List saved jobs"""
    student = get_student_profile(request.user)
    saved_jobs_list = SavedJob.objects.filter(student=student).select_related('job')
    
    paginator = Paginator(saved_jobs_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "student_portal/saved_jobs.html", {'page_obj': page_obj})


# ========== INTERVIEWS ==========

@login_required
def interview_list(request: HttpRequest) -> HttpResponse:
    """List interviews"""
    student = get_student_profile(request.user)
    interviews = Interview.objects.filter(
        application__student=student
    ).select_related('application__job').order_by('scheduled_at')
    
    context = {
        'upcoming': interviews.filter(status='scheduled', scheduled_at__gte=timezone.now()),
        'past': interviews.exclude(status='scheduled'),
    }
    return render(request, "student_portal/interview_list.html", context)


# ========== MESSAGES ==========

@login_required
def message_list(request: HttpRequest) -> HttpResponse:
    """List messages"""
    messages_list = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient').order_by('-sent_at')
    
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "student_portal/message_list.html", {'page_obj': page_obj})


@login_required
def message_send(request: HttpRequest) -> HttpResponse:
    """Send a message"""
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, "Message sent successfully!")
            return redirect('student:message_list')
    else:
        form = MessageForm()
    
    return render(request, "student_portal/message_form.html", {'form': form})


# ========== NOTIFICATIONS ==========

@login_required
def notification_list(request: HttpRequest) -> HttpResponse:
    """List notifications"""
    notifications = Notification.objects.filter(user=request.user)
    
    # Mark as read
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "student_portal/notification_list.html", {'page_obj': page_obj})


# ========== SKILL DEVELOPMENT ==========

@login_required
def skill_gap_analysis(request: HttpRequest) -> HttpResponse:
    """View skill gap analysis"""
    student = get_student_profile(request.user)
    gaps = SkillGapAnalysis.objects.filter(student=student)
    
    return render(request, "student_portal/skill_gap_analysis.html", {'gaps': gaps})


@login_required
def practice_tests(request: HttpRequest) -> HttpResponse:
    """List practice tests"""
    tests = PracticeTest.objects.filter(is_active=True)
    return render(request, "student_portal/practice_tests.html", {'tests': tests})


@login_required
def mock_interview_list(request: HttpRequest) -> HttpResponse:
    """List mock interviews"""
    student = get_student_profile(request.user)
    mock_interviews = MockInterview.objects.filter(student=student)
    
    return render(request, "student_portal/mock_interview_list.html", {'mock_interviews': mock_interviews})


@login_required
def mock_interview_request(request: HttpRequest) -> HttpResponse:
    """Request a mock interview"""
    student = get_student_profile(request.user)
    
    if request.method == 'POST':
        form = MockInterviewForm(request.POST)
        if form.is_valid():
            mock = form.save(commit=False)
            mock.student = student
            mock.save()
            messages.success(request, "Mock interview requested successfully!")
            return redirect('student:mock_interview_list')
    else:
        form = MockInterviewForm()
    
    return render(request, "student_portal/mock_interview_form.html", {'form': form})
