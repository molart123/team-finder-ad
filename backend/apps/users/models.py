import logging
import os
import random
from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont
from team_finder.constants import (
    AVATAR_COLORS,
    AVATAR_FONT_PATH,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)

from .managers import UserManager

logger = logging.getLogger(__name__)


class User(AbstractUser):
    username = None
    objects = UserManager()

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH, verbose_name="Имя")
    surname = models.CharField(
        max_length=USER_SURNAME_MAX_LENGTH, verbose_name="Фамилия"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    phone = models.CharField(
        max_length=USER_PHONE_MAX_LENGTH, blank=True, verbose_name="Телефон"
    )
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    about = models.TextField(
        max_length=USER_ABOUT_MAX_LENGTH, blank=True, null=True, verbose_name="О себе"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    projects = models.ManyToManyField(
        "projects.Project", blank=True, related_name="user_projects"
    )
    favorites = models.ManyToManyField(
        "projects.Project", blank=True, related_name="favorited_by"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    # Чтобы избежать конфликтов с группами и правами по умолчанию
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="users_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="users_user_permissions",
        blank=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname}"

    def generate_avatar(self):
        """Генерирует аватар с инициалом имени на случайном фоне."""
        if self.avatar:
            return

        # Создаём холст
        img = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), random.choice(AVATAR_COLORS))
        draw = ImageDraw.Draw(img)

        # Первая буква имени
        letter = self.name[0].upper() if self.name else "?"

        # Загружаем шрифт (с fallback на встроенный)
        font_path = os.path.join(settings.BASE_DIR, AVATAR_FONT_PATH)
        try:
            font = ImageFont.truetype(font_path, AVATAR_FONT_SIZE)
        except Exception as e:
            logger.warning(
                f"Не удалось загрузить шрифт по пути {font_path}: {e}. "
                "Используется шрифт по умолчанию (буква может быть очень мелкой)."
            )
            font = ImageFont.load_default()
            # Для встроенного шрифта размер фиксирован, поэтому предупреждаем.

        # Центрируем букву
        bbox = draw.textbbox((0, 0), letter, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(
            ((AVATAR_SIZE - w) / 2, (AVATAR_SIZE - h) / 2),
            letter,
            fill=AVATAR_TEXT_COLOR,
            font=font,
        )

        # Сохраняем в буфер и прикрепляем к полю avatar
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.avatar.save(
            f"avatar_{self.pk}.png", ContentFile(buffer.getvalue()), save=False
        )

    def save(self, *args, **kwargs):
        # Для новых пользователей без аватара генерируем его после получения pk
        if not self.pk and not self.avatar:
            super().save(*args, **kwargs)  # сохраняем, чтобы появился pk
            self.generate_avatar()
            super().save(update_fields=["avatar"])  # обновляем только avatar
        else:
            super().save(*args, **kwargs)
