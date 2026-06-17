import random
from io import BytesIO

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from .managers import UserManager


class User(AbstractUser):
    username = None
    objects = UserManager()
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    name = models.CharField(max_length=124, verbose_name="Имя")
    surname = models.CharField(max_length=124, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=12, blank=True, verbose_name="Телефон")
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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def generate_avatar(self):
        if self.avatar:
            return

        colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
        ]
        size = 200
        img = Image.new('RGB', (size, size), random.choice(colors))
        draw = ImageDraw.Draw(img)

        letter = self.name[0].upper() if self.name else '?'
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 80)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), letter, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size - w) / 2, (size - h) / 2), letter, fill='white', font=font)

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        self.avatar.save(f'avatar_{self.pk}.png', ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            super().save(*args, **kwargs)
            self.generate_avatar()
            super().save(update_fields=['avatar'])
        else:
            super().save(*args, **kwargs)



    def __str__(self):
        return f'{self.name} {self.surname}'