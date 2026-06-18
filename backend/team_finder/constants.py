# ===== Пользователь (User) =====
# Длины полей модели User
USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256

# Количество пользователей на странице при пагинации
USERS_PAGINATE_BY = 12

# ===== Проект (Project) =====
# Длины полей модели Project
PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 6

# Статусы проекта
PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"
PROJECT_STATUS_CHOICES = [
    (PROJECT_STATUS_OPEN, "Открыт"),
    (PROJECT_STATUS_CLOSED, "Закрыт"),
]

# Количество проектов на странице при пагинации
PROJECT_PAGINATE_BY = 12


# ===== Генерация аватара пользователя =====
# Настройки для генерации аватарок (используются в users/models.py)
AVATAR_COLORS = [
    "#FF6B6B",
    "#4ECDC4",
    "#45B7D1",
    "#96CEB4",
    "#FFEAA7",
    "#DDA0DD",
    "#98D8C8",
    "#F7DC6F",
    "#BB8FCE",
    "#85C1E9",
]
AVATAR_SIZE = 200
AVATAR_TEXT_COLOR = "white"
AVATAR_FONT_SIZE = 80


AVATAR_FONT_PATH = "static/fonts/DejaVuSans-Bold.ttf"
