"""
Forms for TPO Portal: student eligibility, application status, interview scheduling.
"""
from django import forms

from student_portal.models import StudentProfile, Application, Interview


class StudentEligibilityForm(forms.ModelForm):
    """Toggle placement eligibility for a student."""

    class Meta:
        model = StudentProfile
        fields = ["placement_eligible"]
        widgets = {"placement_eligible": forms.CheckboxInput(attrs={"class": "form-check-input"})}


class ApplicationStatusForm(forms.ModelForm):
    """Update application status."""

    class Meta:
        model = Application
        fields = ["status"]
        widgets = {"status": forms.Select(attrs={"class": "form-select"})}


class InterviewScheduleForm(forms.ModelForm):
    """Schedule or update interview."""

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
