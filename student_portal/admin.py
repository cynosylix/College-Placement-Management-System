from django.contrib import admin
from .models import (
    StudentProfile, Skill, Certification, Resume, PortfolioItem,
    Document, JobPosting, Application, SavedJob, Interview,
    Message, Notification, SkillGapAnalysis, PracticeTest, MockInterview
)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'enrollment_number', 'course', 'branch', 'cgpa', 'created_at']
    list_filter = ['course', 'branch', 'year']
    search_fields = ['user__username', 'enrollment_number', 'user__email']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'proficiency_level']
    list_filter = ['proficiency_level']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'issuer', 'issue_date']


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['student', 'title', 'is_default', 'created_at']
    list_filter = ['is_default']


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['student', 'title', 'project_type', 'date_completed']
    list_filter = ['project_type']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'document_type', 'uploaded_at']
    list_filter = ['document_type']


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'job_type', 'posted_by', 'posted_at', 'is_active']
    list_filter = ['job_type', 'is_active', 'posted_at']
    search_fields = ['title', 'company_name', 'description']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['student__user__username', 'job__title']


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['student', 'job', 'saved_at']


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'scheduled_at', 'status', 'location']
    list_filter = ['status', 'scheduled_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'sent_at']
    list_filter = ['is_read', 'sent_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']


@admin.register(SkillGapAnalysis)
class SkillGapAnalysisAdmin(admin.ModelAdmin):
    list_display = ['student', 'required_skill', 'gap_status']
    list_filter = ['gap_status']


@admin.register(PracticeTest)
class PracticeTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'test_type', 'duration_minutes', 'is_active']
    list_filter = ['test_type', 'is_active']


@admin.register(MockInterview)
class MockInterviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'preferred_date', 'status', 'requested_at']
    list_filter = ['status', 'requested_at']
