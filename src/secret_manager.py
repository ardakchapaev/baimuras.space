"""
Система управления секретами для BaiMuras Platform
Обеспечивает безопасное управление конфиденциальными данными
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class SecretConfig:
    """Конфигурация для управления секретами"""

    required_secrets: list
    optional_secrets: dict
    env_file_path: Optional[str] = None


class SecretManager:
    """
    Менеджер для безопасного управления секретами приложения

    Функции:
    - Загрузка секретов из переменных окружения
    - Валидация обязательных секретов
    - Безопасное логирование (маскирование секретов)
    - Поддержка .env файлов
    """

    def __init__(self, config: SecretConfig):
        self.config = config
        self.secrets: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)

        # Загружаем .env файл если указан
        if config.env_file_path and Path(config.env_file_path).exists():
            self._load_env_file(config.env_file_path)

        # Загружаем секреты
        self._load_secrets()

        # Валидируем обязательные секреты
        self._validate_required_secrets()

    def _load_env_file(self, env_path: str) -> None:
        """Загружает переменные из .env файла"""
        try:
            from dotenv import load_dotenv

            load_dotenv(env_path)
            self.logger.info(f"Загружен .env файл: {env_path}")
        except ImportError:
            self.logger.warning("python-dotenv не установлен, .env файл не загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки .env файла: {e}")

    def _load_secrets(self) -> None:
        """Загружает секреты из переменных окружения"""
        # Загружаем обязательные секреты
        for secret_name in self.config.required_secrets:
            value = os.getenv(secret_name)
            if value is not None:
                self.secrets[secret_name] = value

        # Загружаем опциональные секреты с значениями по умолчанию
        for secret_name, default_value in self.config.optional_secrets.items():
            value = os.getenv(secret_name, default_value)
            self.secrets[secret_name] = value

    def _validate_required_secrets(self) -> None:
        """Валидирует наличие всех обязательных секретов"""
        missing_secrets = []

        for secret_name in self.config.required_secrets:
            if secret_name not in self.secrets or not self.secrets[secret_name]:
                missing_secrets.append(secret_name)

        if missing_secrets:
            error_msg = f"Отсутствуют обязательные переменные окружения: {', '.join(missing_secrets)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.logger.info(
            f"Все обязательные секреты загружены успешно ({len(self.config.required_secrets)} шт.)"
        )

    def get_secret(self, name: str, default: Any = None) -> Any:
        """
        Получает значение секрета по имени

        Args:
            name: Имя секрета
            default: Значение по умолчанию

        Returns:
            Значение секрета или default
        """
        return self.secrets.get(name, default)

    def get_database_url(self) -> str:
        """Формирует URL базы данных из компонентов"""
        db_type = self.get_secret("DATABASE_TYPE", "sqlite")

        if db_type.lower() == "sqlite":
            db_path = self.get_secret("DATABASE_PATH", "instance/baimuras.db")
            return f"sqlite:///{db_path}"

        elif db_type.lower() == "postgresql":
            user = self.get_secret("DATABASE_USER")
            password = self.get_secret("DATABASE_PASSWORD")
            host = self.get_secret("DATABASE_HOST", "localhost")
            port = self.get_secret("DATABASE_PORT", "5432")
            name = self.get_secret("DATABASE_NAME")

            if not all([user, password, name]):
                raise ValueError(
                    "Для PostgreSQL требуются DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME"
                )

            return f"postgresql://{user}:{password}@{host}:{port}/{name}"

        else:
            raise ValueError(f"Неподдерживаемый тип базы данных: {db_type}")

    def get_redis_url(self) -> str:
        """Формирует URL Redis из компонентов"""
        host = self.get_secret("REDIS_HOST", "localhost")
        port = self.get_secret("REDIS_PORT", "6379")
        db = self.get_secret("REDIS_DB", "0")
        password = self.get_secret("REDIS_PASSWORD")

        if password:
            return f"redis://:{password}@{host}:{port}/{db}"
        else:
            return f"redis://{host}:{port}/{db}"

    def mask_secret(self, value: str, show_chars: int = 4) -> str:
        """
        Маскирует секрет для безопасного логирования

        Args:
            value: Значение для маскирования
            show_chars: Количество символов для показа в начале и конце

        Returns:
            Замаскированное значение
        """
        if not value or len(value) <= show_chars * 2:
            return "*" * len(value) if value else ""

        return f"{value[:show_chars]}{'*' * (len(value) - show_chars * 2)}{value[-show_chars:]}"

    def get_config_summary(self) -> Dict[str, str]:
        """
        Возвращает сводку конфигурации с замаскированными секретами
        для безопасного логирования
        """
        summary = {}

        for name, value in self.secrets.items():
            if isinstance(value, str) and any(
                keyword in name.upper()
                for keyword in ["PASSWORD", "SECRET", "KEY", "TOKEN", "API"]
            ):
                summary[name] = self.mask_secret(value)
            else:
                summary[name] = str(value)

        return summary


# Предустановленные конфигурации для разных сред
def get_development_config() -> SecretConfig:
    """Конфигурация для разработки"""
    return SecretConfig(
        required_secrets=["SECRET_KEY", "JWT_SECRET_KEY"],
        optional_secrets={
            "DATABASE_TYPE": "sqlite",
            "DATABASE_PATH": "instance/baimuras.db",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "REDIS_DB": "0",
            "MAIL_SERVER": "localhost",
            "MAIL_PORT": "587",
            "MAIL_USE_TLS": "True",
            "MAIL_USERNAME": "",
            "MAIL_PASSWORD": "",
            "CELERY_BROKER_URL": "redis://localhost:6379/0",
            "CELERY_RESULT_BACKEND": "redis://localhost:6379/0",
            "N8N_WEBHOOK_URL": "",
            "FLASK_ENV": "development",
            "DEBUG": "True",
        },
        env_file_path=".env",
    )


def get_production_config() -> SecretConfig:
    """Конфигурация для продакшн"""
    return SecretConfig(
        required_secrets=[
            "SECRET_KEY",
            "JWT_SECRET_KEY",
            "DATABASE_USER",
            "DATABASE_PASSWORD",
            "DATABASE_NAME",
            "MAIL_USERNAME",
            "MAIL_PASSWORD",
        ],
        optional_secrets={
            "DATABASE_TYPE": "postgresql",
            "DATABASE_HOST": "localhost",
            "DATABASE_PORT": "5432",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "REDIS_DB": "0",
            "REDIS_PASSWORD": "",
            "MAIL_SERVER": "smtp.gmail.com",
            "MAIL_PORT": "587",
            "MAIL_USE_TLS": "True",
            "CELERY_BROKER_URL": "",
            "CELERY_RESULT_BACKEND": "",
            "N8N_WEBHOOK_URL": "",
            "FLASK_ENV": "production",
            "DEBUG": "False",
        },
    )


def get_testing_config() -> SecretConfig:
    """Конфигурация для тестирования"""
    return SecretConfig(
        required_secrets=["SECRET_KEY", "JWT_SECRET_KEY"],
        optional_secrets={
            "DATABASE_TYPE": "sqlite",
            "DATABASE_PATH": ":memory:",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "REDIS_DB": "1",
            "MAIL_SERVER": "localhost",
            "MAIL_PORT": "587",
            "MAIL_USE_TLS": "False",
            "MAIL_USERNAME": "test@example.com",
            "MAIL_PASSWORD": "testpass",
            "CELERY_BROKER_URL": "redis://localhost:6379/1",
            "CELERY_RESULT_BACKEND": "redis://localhost:6379/1",
            "FLASK_ENV": "testing",
            "DEBUG": "True",
            "TESTING": "True",
        },
    )
