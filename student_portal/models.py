from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class StudentProfile(models.Model):
    """Extended student profile with academic and personal details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    # Personal Information
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Academic Information
    enrollment_number = models.CharField(max_length=50, unique=True, blank=True)
    course = models.CharField(max_length=100, blank=True)  # B.Tech, M.Tech, etc.
    branch = models.CharField(max_length=100, blank=True)  # CSE, ECE, etc.
    year = models.CharField(max_length=20, blank=True)  # 1st, 2nd, 3rd, 4th
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    
    # Additional Details
    bio = models.TextField(blank=True, help_text="Brief introduction about yourself")
    achievements = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"
    
    def __str__(self):
        return f"{self.user.username} - {self.enrollment_number}"


class Skill(models.Model):
    """Student skills"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    
    def __str__(self):
        return f"{self.student.user.username} - {self.name}"


class Certification(models.Model):
    """Student certifications"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.name}"


class Resume(models.Model):
    """Multiple resume versions for a student"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, help_text="e.g., Software Engineer Resume, Data Science Resume")
    content = models.TextField(help_text="Resume content in JSON or formatted text")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.title}"


class PortfolioItem(models.Model):
    """Portfolio projects, GitHub links, publications"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(
        max_length=50,
        choices=[
            ('project', 'Project'),
            ('github', 'GitHub Repository'),
            ('publication', 'Publication'),
            ('other', 'Other'),
        ],
        default='project'
    )
    url = models.URLField(blank=True)
    technologies = models.CharField(max_length=500, blank=True, help_text="Comma-separated technologies")
    date_completed = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.title}"


class Document(models.Model):
    """Uploaded documents: transcripts, certificates, ID proofs"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=200)
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('transcript', 'Transcript'),
            ('certificate', 'Certificate'),
            ('id_proof', 'ID Proof'),
            ('photo', 'Photo'),
            ('other', 'Other'),
        ]
    )
    file = models.FileField(upload_to='student_documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.name}"


class JobPosting(models.Model):
    """Job/Internship postings from recruiters"""
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(help_text="Required skills, qualifications, etc.")
    location = models.CharField(max_length=200, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('internship', 'Internship'),
            ('contract', 'Contract'),
        ],
        default='full_time'
    )
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_postings')
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-posted_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.title}"


class Application(models.Model):
    """Student job applications"""
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'job']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.job.title}"


class SavedJob(models.Model):
    """Bookmarked jobs for later"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'job']
        ordering = ['-saved_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.job.title}"


class Interview(models.Model):
    """Interview schedules"""
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='interview')
    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('rescheduled', 'Rescheduled'),
        ],
        default='scheduled'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['scheduled_at']
    
    def __str__(self):
        return f"Interview - {self.application.student.user.username}"


class Message(models.Model):
    """Messages between students, TPO, and recruiters"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.subject}"


class Notification(models.Model):
    """System notifications for students"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        choices=[
            ('job_alert', 'Job Alert'),
            ('interview', 'Interview'),
            ('application_update', 'Application Update'),
            ('announcement', 'Announcement'),
            ('message', 'Message'),
        ]
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class SkillGapAnalysis(models.Model):
    """Skill gap analysis for students"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skill_gaps')
    required_skill = models.CharField(max_length=100)
    current_level = models.CharField(max_length=20, blank=True)
    required_level = models.CharField(max_length=20)
    gap_status = models.CharField(
        max_length=20,
        choices=[
            ('met', 'Met'),
            ('gap', 'Gap Identified'),
            ('exceeded', 'Exceeded'),
        ],
        default='gap'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.required_skill}"


class PracticeTest(models.Model):
    """Practice tests for skill development"""
    title = models.CharField(max_length=200)
    test_type = models.CharField(
        max_length=50,
        choices=[
            ('aptitude', 'Aptitude'),
            ('technical', 'Technical'),
            ('psychometric', 'Psychometric'),
            ('coding', 'Coding'),
        ]
    )
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class MockInterview(models.Model):
    """Mock interview requests"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='mock_interviews')
    requested_at = models.DateTimeField(auto_now_add=True)
    preferred_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('requested', 'Requested'),
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='requested'
    )
    feedback = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"Mock Interview - {self.student.user.username}"
