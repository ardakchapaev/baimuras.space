"""
Безопасная конфигурация для BaiMuras Platform с использованием SecretManager
"""

import logging
import os
from datetime import timedelta

from .secret_manager import (
    SecretManager,
    get_development_config,
    get_production_config,
    get_testing_config,
)


class BaseConfig:
    """Базовая конфигурация с использованием SecretManager"""

    def __init__(self):
        # Определяем среду выполнения
        self.environment = os.getenv("FLASK_ENV", "development").lower()

        # Выбираем конфигурацию секретов в зависимости от среды
        if self.environment == "production":
            secret_config = get_production_config()
        elif self.environment == "testing":
            secret_config = get_testing_config()
        else:
            secret_config = get_development_config()

        # Инициализируем менеджер секретов
        self.secret_manager = SecretManager(secret_config)

        # Настраиваем логирование
        self._setup_logging()

        # Загружаем конфигурацию
        self._load_config()

    def _setup_logging(self):
        """Настройка логирования"""
        log_level = (
            logging.DEBUG
            if self.secret_manager.get_secret("DEBUG", "False").lower() == "true"
            else logging.INFO
        )

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                (
                    logging.FileHandler("logs/baimuras.log")
                    if os.path.exists("logs")
                    else logging.NullHandler()
                ),
            ],
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Инициализация конфигурации для среды: {self.environment}")

    def _load_config(self):
        """Загрузка основных параметров конфигурации"""
        # Flask основные настройки
        self.SECRET_KEY = self.secret_manager.get_secret("SECRET_KEY")
        self.DEBUG = self.secret_manager.get_secret("DEBUG", "False").lower() == "true"
        self.TESTING = (
            self.secret_manager.get_secret("TESTING", "False").lower() == "true"
        )

        # База данных
        self.SQLALCHEMY_DATABASE_URI = self.secret_manager.get_database_url()
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }

        # JWT настройки
        self.JWT_SECRET_KEY = self.secret_manager.get_secret("JWT_SECRET_KEY")
        self.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
        self.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

        # Redis и Celery
        redis_url = self.secret_manager.get_redis_url()
        self.CELERY_BROKER_URL = self.secret_manager.get_secret(
            "CELERY_BROKER_URL", redis_url
        )
        self.CELERY_RESULT_BACKEND = self.secret_manager.get_secret(
            "CELERY_RESULT_BACKEND", redis_url
        )

        # Настройки почты
        self.MAIL_SERVER = self.secret_manager.get_secret("MAIL_SERVER")
        self.MAIL_PORT = int(self.secret_manager.get_secret("MAIL_PORT", "587"))
        self.MAIL_USE_TLS = (
            self.secret_manager.get_secret("MAIL_USE_TLS", "True").lower() == "true"
        )
        self.MAIL_USERNAME = self.secret_manager.get_secret("MAIL_USERNAME")
        self.MAIL_PASSWORD = self.secret_manager.get_secret("MAIL_PASSWORD")
        self.MAIL_DEFAULT_SENDER = self.MAIL_USERNAME

        # Безопасность
        self.WTF_CSRF_ENABLED = True
        self.WTF_CSRF_TIME_LIMIT = 3600

        # Rate limiting
        self.RATELIMIT_STORAGE_URL = redis_url
        self.RATELIMIT_DEFAULT = "100 per hour"

        # Интеграции
        self.N8N_WEBHOOK_URL = self.secret_manager.get_secret("N8N_WEBHOOK_URL")

        # Логирование конфигурации (с маскированием секретов)
        config_summary = self.secret_manager.get_config_summary()
        self.logger.info("Конфигурация загружена успешно")
        self.logger.debug(f"Сводка конфигурации: {config_summary}")


class DevelopmentConfig(BaseConfig):
    """Конфигурация для разработки"""

    def __init__(self):
        super().__init__()
        self.DEBUG = True

        # Дополнительные настройки для разработки
        self.SQLALCHEMY_ECHO = True  # Логирование SQL запросов
        self.WTF_CSRF_ENABLED = False  # Отключаем CSRF для удобства разработки

        self.logger.info("Загружена конфигурация для разработки")


class ProductionConfig(BaseConfig):
    """Конфигурация для продакшн"""

    def __init__(self):
        super().__init__()
        self.DEBUG = False

        # Продакшн настройки безопасности
        self.SESSION_COOKIE_SECURE = True
        self.SESSION_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SAMESITE = "Lax"

        # Настройки Talisman для безопасности
        self.TALISMAN_CONFIG = {
            "force_https": True,
            "strict_transport_security": True,
            "strict_transport_security_max_age": 31536000,
            "content_security_policy": {
                "default-src": "'self'",
                "script-src": "'self' 'unsafe-inline'",
                "style-src": "'self' 'unsafe-inline'",
                "img-src": "'self' data: https:",
                "font-src": "'self'",
                "connect-src": "'self'",
                "frame-ancestors": "'none'",
            },
        }

        # Более строгие настройки базы данных
        self.SQLALCHEMY_ENGINE_OPTIONS.update(
            {
                "pool_size": 10,
                "max_overflow": 20,
                "pool_timeout": 30,
            }
        )

        self.logger.info("Загружена конфигурация для продакшн")


class TestingConfig(BaseConfig):
    """Конфигурация для тестирования"""

    def __init__(self):
        super().__init__()
        self.TESTING = True
        self.DEBUG = True

        # Настройки для тестирования
        self.WTF_CSRF_ENABLED = False
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

        self.logger.info("Загружена конфигурация для тестирования")


# Фабрика конфигураций
def get_config(environment: str = None) -> BaseConfig:
    """
    Возвращает конфигурацию для указанной среды

    Args:
        environment: Среда выполнения ('development', 'production', 'testing')

    Returns:
        Экземпляр соответствующей конфигурации
    """
    if environment is None:
        environment = os.getenv("FLASK_ENV", "development").lower()

    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_class = config_map.get(environment, DevelopmentConfig)
    return config_class()
