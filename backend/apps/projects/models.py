from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',   # <-- исправлено
        verbose_name="Автор проекта"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    status = models.CharField(
        max_length=6,
        choices=[('open', 'Открыт'), ('closed', 'Закрыт')],
        default='open',
        verbose_name="Статус"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',   # правильно
        verbose_name="Участники"
    )

    def __str__(self):
        return self.name