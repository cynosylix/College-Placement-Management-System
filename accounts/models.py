from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        STUDENT = "student", "Student"
        TPO = "tpo", "Training & Placement Officer"
        RECRUITER = "recruiter", "Recruiter"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.UNKNOWN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.role})"
