import re

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from team_finder.constants import (
    USER_NAME_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)

from ..common.mixins import GitHubValidationMixin
from .models import User


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=USER_NAME_MAX_LENGTH, widget=forms.TextInput)
    surname = forms.CharField(
        max_length=USER_SURNAME_MAX_LENGTH, widget=forms.TextInput
    )


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UpdateForm(GitHubValidationMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "phone", "avatar", "about", "github_url"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            cleaned = re.sub(r"\D", "", phone)
            if not (
                (phone.startswith("8") and len(cleaned) == 11)
                or (phone.startswith("+7") and len(cleaned) == 11)
            ):
                raise ValidationError(
                    "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
                )
            if phone.startswith("8"):
                normalized = "+7" + cleaned[1:]
            else:
                normalized = "+7" + cleaned[1:]
            if (
                User.objects.exclude(pk=self.instance.pk)
                .filter(phone=normalized)
                .exists()
            ):
                raise ValidationError("Этот номер уже используется")
            return normalized
        return phone


class CustomPasswordChangeForm(PasswordChangeForm):
    pass
