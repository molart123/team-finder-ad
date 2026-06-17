from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания проекта")
    github_url = models.URLField(null=True, blank=True, verbose_name="Ссылка на github проекта")
    status = models.CharField(
        choices=[("open", "Open"), ("closed", "Closed")],
        max_length=6,
        default="open",
        verbose_name="Статус проекта"
    )
    owner = models.ForeignKey(
        "users.User",
        blank=False,
        on_delete=models.CASCADE,
        related_name="owner",
        verbose_name="Автор проекта"
    )
    participants = models.ManyToManyField(
        "users.User",
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники проекта"
    )