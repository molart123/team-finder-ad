from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager

class User(AbstractUser):
    username = None
    objects = UserManager()
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    name = models.CharField(max_length=124, verbose_name="Имя")
    surname = models.CharField(max_length=124, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=12, blank=True,verbose_name="Телефон")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    about = models.TextField(max_length=256, blank=True, null=True, verbose_name="О себе")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    projects = models.ManyToManyField('projects.Project', blank=True, related_name='user_projects')
    favorites_projects = models.ManyToManyField('projects.Project', blank=True, related_name='favorited_by')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_user_permissions',
        blank=True,
    )

    def __str__(self):
        return f'{self.name} {self.surname}'