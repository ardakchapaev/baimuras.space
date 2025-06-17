"""Module docstring."""

import os

from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class Config:
    """Class docstring."""

    # Безопасный SECRET_KEY
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        if os.environ.get("FLASK_ENV") == "production":
            raise RuntimeError(
                "SECRET_KEY environment variable must be set in production"
            )
        else:
            # Для разработки генерируем временный ключ
            import secrets

            SECRET_KEY = secrets.token_hex(32)
            print(
                "WARNING: Using generated SECRET_KEY for development. Set SECRET_KEY environment variable for production."
            )

    # База данных
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///baimuras.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF защита
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 час

    # Настройки для API
    API_KEY = os.environ.get("API_KEY") or "dev-api-key-change-in-production"

    # Настройки почты (для будущего использования)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
