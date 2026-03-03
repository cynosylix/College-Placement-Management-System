"""
Forms for Recruiter Portal: job postings and application workflow.
"""
from django import forms
from django.utils import timezone

from student_portal.models import JobPosting, Application, Interview


class JobPostingForm(forms.ModelForm):
    """Create/Edit job posting."""

    class Meta:
        model = JobPosting
        fields = [
            "title",
            "company_name",
            "description",
            "requirements",
            "location",
            "salary_range",
            "min_cgpa",
            "eligibility_criteria",
            "job_type",
            "application_deadline",
            "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Job title"}),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "requirements": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "salary_range": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 8-12 LPA"}),
            "min_cgpa": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "10"}),
            "eligibility_criteria": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "application_deadline": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_application_deadline(self):
        value = self.cleaned_data.get("application_deadline")
        if value and value <= timezone.now():
            raise forms.ValidationError("Deadline must be in the future.")
        return value


class ApplicationStatusForm(forms.ModelForm):
    """Update application status (shortlist, reject, etc.)."""

    class Meta:
        model = Application
        fields = ["status"]
        widgets = {"status": forms.Select(attrs={"class": "form-select"})}


class InterviewScheduleForm(forms.ModelForm):
    """Schedule or update interview for an application."""

    class Meta:
        model = Interview
        fields = ["scheduled_at", "location", "meeting_link", "notes", "status"]
        widgets = {
            "scheduled_at": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "meeting_link": forms.URLInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
