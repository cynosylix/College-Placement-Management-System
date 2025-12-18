from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"autocomplete": "email"}))

    role: str | None = None

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Ensure profile exists even if signals are disabled in some environments.
            profile, _ = Profile.objects.get_or_create(user=user)
            if self.role:
                profile.role = self.role
                profile.save(update_fields=["role"])
        return user


class StudentRegistrationForm(RegistrationForm):
    role = Profile.Role.STUDENT


class TpoRegistrationForm(RegistrationForm):
    role = Profile.Role.TPO


class RecruiterRegistrationForm(RegistrationForm):
    role = Profile.Role.RECRUITER


