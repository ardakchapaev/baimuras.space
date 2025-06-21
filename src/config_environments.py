"""
Конфигурации для разных сред развертывания
"""
import os
from datetime import timedelta


class BaseConfig:
    """Базовая конфигурация"""

    # Основные настройки
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for development config")

    # База данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # JWT настройки
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'

    # Email настройки
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in [
        'true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get(
        'MAIL_DEFAULT_SENDER') or 'info@baimuras.space'

    # Celery настройки
    CELERY_BROKER_URL = os.environ.get(
        'CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get(
        'CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

    # n8n настройки
    N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')
    N8N_API_URL = os.environ.get(
        'N8N_API_URL') or 'http://localhost:5678/api/v1'
    N8N_API_KEY = os.environ.get('N8N_API_KEY')
    N8N_WEBHOOK_SECRET = os.environ.get('N8N_WEBHOOK_SECRET')
    N8N_TIMEOUT = int(os.environ.get('N8N_TIMEOUT', '30'))

    # Файловые настройки
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Безопасность
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Логирование
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/baimuras.log'

    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get(
        'RATELIMIT_STORAGE_URL') or 'redis://localhost:6379/1'

    # Языки
    LANGUAGES = ['ru', 'ky']
    DEFAULT_LANGUAGE = 'ru'

    # Пагинация
    POSTS_PER_PAGE = 20
    MAX_SEARCH_RESULTS = 50


class DevelopmentConfig(BaseConfig):
    """Конфигурация для разработки"""

    DEBUG = True
    TESTING = False

    # База данных для разработки
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + \
        os.path.join(os.path.dirname(os.path.dirname(__file__)),
                     'instance', 'baimuras_dev.db')

    # Отключение HTTPS для разработки
    PREFERRED_URL_SCHEME = 'http'

    # Более подробное логирование
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'

    # CORS для разработки
    CORS_ORIGINS = ['http://localhost:3000',
                    'http://localhost:3001', 'http://127.0.0.1:3000']

    # Отключение некоторых проверок безопасности для разработки
    WTF_CSRF_ENABLED = False

    # Email в консоль для разработки
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = True


class TestingConfig(BaseConfig):
    """Конфигурация для тестирования"""

    DEBUG = False
    TESTING = True

    # In-memory база данных для тестов
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Отключение CSRF для тестов
    WTF_CSRF_ENABLED = False

    # Отключение email для тестов
    MAIL_SUPPRESS_SEND = True

    # Быстрые JWT токены для тестов
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)

    # Отключение rate limiting для тестов
    RATELIMIT_ENABLED = False


class StagingConfig(BaseConfig):
    """Конфигурация для staging окружения"""

    DEBUG = False
    TESTING = False

    # База данных staging
    SQLALCHEMY_DATABASE_URI = os.environ.get('STAGING_DATABASE_URL') or \
        'postgresql://user:password@localhost/baimuras_staging'

    # HTTPS для staging
    PREFERRED_URL_SCHEME = 'https'

    # Логирование в файл
    LOG_LEVEL = 'INFO'

    # CORS для staging
    CORS_ORIGINS = ['https://staging.baimuras.space',
                    'https://hub-staging.baimuras.space']

    # Email настройки для staging
    MAIL_SUPPRESS_SEND = False


class ProductionConfig(BaseConfig):
    """Конфигурация для продакшена"""

    DEBUG = False
    TESTING = False

    # База данных продакшена
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/baimuras_production'

    # HTTPS обязательно для продакшена
    PREFERRED_URL_SCHEME = 'https'

    # Строгие настройки безопасности
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production config")

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("No JWT_SECRET_KEY set for production config")

    # Логирование
    LOG_LEVEL = 'WARNING'
    SQLALCHEMY_ECHO = False

    # CORS для продакшена
    CORS_ORIGINS = ['https://baimuras.space', 'https://hub.baimuras.space']

    # Email настройки продакшена
    MAIL_SUPPRESS_SEND = False

    # Более длительные JWT токены для продакшена
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Строгий rate limiting
    RATELIMIT_DEFAULT = "100 per hour"


class DockerConfig(BaseConfig):
    """Конфигурация для Docker контейнеров"""

    DEBUG = False
    TESTING = False

    # База данных через Docker
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:password@db:5432/baimuras'

    # Redis через Docker
    CELERY_BROKER_URL = os.environ.get(
        'CELERY_BROKER_URL') or 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get(
        'CELERY_RESULT_BACKEND') or 'redis://redis:6379/0'
    RATELIMIT_STORAGE_URL = os.environ.get(
        'RATELIMIT_STORAGE_URL') or 'redis://redis:6379/1'

    # n8n через Docker
    N8N_API_URL = os.environ.get('N8N_API_URL') or 'http://n8n:5678/api/v1'

    # Логирование в stdout для Docker
    LOG_TO_STDOUT = True


# Словарь конфигураций
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """
    Получение конфигурации по имени

    Args:
        config_name: Имя конфигурации

    Returns:
        Класс конфигурации
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    return config.get(config_name, config['default'])
