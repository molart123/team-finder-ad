from django.core.exceptions import ValidationError


class GitHubValidationMixin:
    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url:
            if not url.startswith("https://github.com/"):
                raise ValidationError("Ссылка должна вести на github.com")
        return url
