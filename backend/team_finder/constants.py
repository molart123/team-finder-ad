from enum import StrEnum

# ===== Пользователь (User) =====
USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256

USERS_PAGINATE_BY = 12

# ===== Проект (Project) =====
PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 6

PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"
PROJECT_STATUS_CHOICES = [
    (PROJECT_STATUS_OPEN, "Открыт"),
    (PROJECT_STATUS_CLOSED, "Закрыт"),
]

PROJECT_PAGINATE_BY = 12


# ===== Генерация аватара пользователя =====
class AvatarColor(StrEnum):
    """Именованные цвета для генерации аватаров."""

    RED = "#FF6B6B"
    TEAL = "#4ECDC4"
    LIGHT_BLUE = "#45B7D1"
    SAGE = "#96CEB4"
    LIGHT_YELLOW = "#FFEAA7"
    PLUM = "#DDA0DD"
    MINT = "#98D8C8"
    GOLDENROD = "#F7DC6F"
    LAVENDER = "#BB8FCE"
    SKY_BLUE = "#85C1E9"


AVATAR_COLORS = [color.value for color in AvatarColor]

AVATAR_SIZE = 200
AVATAR_TEXT_COLOR = "white"
AVATAR_FONT_SIZE = 80

AVATAR_FONT_PATH = "static/fonts/DejaVuSans-Bold.ttf"
