from django import forms
from team_finder.constants import PROJECT_NAME_MAX_LENGTH

from ..common.mixins import GitHubValidationMixin
from .models import Project


class ProjectForm(GitHubValidationMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Явно задаём max_length для поля name из константы,
        # чтобы видеть использование констант в форме
        self.fields["name"].max_length = PROJECT_NAME_MAX_LENGTH
