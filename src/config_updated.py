
"""Обновленная конфигурация для мебельной платформы BaiMuras."""

import os
from datetime import timedelta

class Config:
    """Базовая конфигурация."""
    
    # Основные настройки Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-baimuras-furniture-platform-2025'
    
    # База данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///baimuras_furniture.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Flask-Mail настройки
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'info@baimuras.space'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'BaiMuras <info@baimuras.space>'
    
    # Celery настройки
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Загрузка файлов
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'dwg'}
    
    # Безопасность
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 час
    BCRYPT_LOG_ROUNDS = 12
    
    # Session настройки
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Установить True для HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/1'
    RATELIMIT_DEFAULT = '1000 per hour'
    
    # Локализация
    LANGUAGES = {
        'ru': 'Русский',
        'ky': 'Кыргызча'
    }
    DEFAULT_LANGUAGE = 'ru'
    
    # Файловое хранилище
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # Логирование
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/baimuras.log'
    
    # API настройки
    API_RATE_LIMIT = '100 per hour'
    API_TOKEN_EXPIRATION = 3600  # 1 час
    
    # Мебельные константы
    FURNITURE_BASE_PRICES = {
        'kitchen': 25000,
        'wardrobe': 18000,
        'children_room': 15000,
        'montessori': 12000,
        'office': 20000,
        'living_room': 22000
    }
    
    MATERIAL_MULTIPLIERS = {
        'laminate': 1.0,
        'mdf': 1.3,
        'natural_wood': 2.0,
        'acrylic': 1.8
    }
    
    COMPLEXITY_MULTIPLIERS = {
        'simple': 0.8,
        'standard': 1.0,
        'complex': 1.3,
        'premium': 1.6
    }
    
    # Контактные данные
    COMPANY_INFO = {
        'name': 'BaiMuras',
        'full_name': 'ИП Чапаев Арстан Бакытович',
        'phone': '+996 509 912 569',
        'email': 'info@baimuras.space',
        'address': 'г. Бишкек, ул. Фрунзе 123, Мебельный центр "Доника", 2 этаж',
        'working_hours': {
            'weekdays': 'Пн-Пт: 9:00-18:00',
            'saturday': 'Сб: 10:00-16:00',
            'sunday': 'Вс: выходной'
        },
        'social_media': {
            'instagram': 'https://instagram.com/baimuras',
            'telegram': 'https://t.me/baimuras',
            'whatsapp': 'https://wa.me/996509912569'
        }
    }
    
    # Настройки уведомлений
    NOTIFICATION_SETTINGS = {
        'new_lead_notification': True,
        'project_status_updates': True,
        'measurement_reminders': True,
        'email_notifications': True,
        'sms_notifications': False  # Пока отключено
    }
    
    @staticmethod
    def init_app(app):
        """Инициализация приложения с конфигурацией."""
        pass

class DevelopmentConfig(Config):
    """Конфигурация для разработки."""
    
    DEBUG = True
    TESTING = False
    
    # Более детальное логирование
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'
    
    # Отключаем некоторые проверки безопасности для разработки
    WTF_CSRF_ENABLED = False
    
    # Локальная база данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev_baimuras.db'
    
    @classmethod
    def init_app(cls, app):
        """Инициализация для разработки."""
        Config.init_app(app)
        
        # Дополнительные настройки для разработки
        import logging
        logging.basicConfig(level=logging.DEBUG)

class TestingConfig(Config):
    """Конфигурация для тестирования."""
    
    TESTING = True
    DEBUG = True
    
    # Тестовая база данных в памяти
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Отключаем CSRF для тестов
    WTF_CSRF_ENABLED = False
    
    # Ускоренная работа bcrypt для тестов
    BCRYPT_LOG_ROUNDS = 4
    
    # Отключаем rate limiting для тестов
    RATELIMIT_ENABLED = False

class ProductionConfig(Config):
    """Конфигурация для продакшена."""
    
    DEBUG = False
    TESTING = False
    
    # Строгие настройки безопасности
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    
    # Продакшен база данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://baimuras_user:password@localhost/baimuras_production'
    
    # Продакшен настройки email
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
    # Продакшен Redis
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    @classmethod
    def init_app(cls, app):
        """Инициализация для продакшена."""
        Config.init_app(app)
        
        # Настройка логирования для продакшена
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/baimuras.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('BaiMuras Furniture Platform startup')

# Маппинг конфигураций
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Дополнительные константы
class FurnitureConstants:
    """Константы для мебельной платформы."""
    
    # Статусы заказов
    ORDER_STATUSES = [
        ('draft', 'Черновик'),
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('in_production', 'В производстве'),
        ('ready', 'Готов'),
        ('delivered', 'Доставлен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен')
    ]
    
    # Статусы проектов
    PROJECT_STATUSES = [
        ('consultation', 'Консультация'),
        ('measurement', 'Замер'),
        ('design', 'Проектирование'),
        ('approval', 'Утверждение'),
        ('production', 'Производство'),
        ('installation', 'Установка'),
        ('completed', 'Завершен')
    ]
    
    # Типы мебели
    FURNITURE_TYPES = [
        ('kitchen', 'Кухня'),
        ('wardrobe', 'Шкаф'),
        ('children_room', 'Детская мебель'),
        ('montessori', 'Мебель Монтессори'),
        ('office', 'Офисная мебель'),
        ('living_room', 'Гостиная'),
        ('custom', 'Индивидуальный проект')
    ]
    
    # Материалы
    MATERIALS = [
        ('laminate', 'ЛДСП'),
        ('mdf', 'МДФ'),
        ('natural_wood', 'Натуральное дерево'),
        ('acrylic', 'Акрил'),
        ('glass', 'Стекло'),
        ('metal', 'Металл')
    ]
    
    # Единицы измерения
    MEASUREMENT_UNITS = [
        ('sq_meter', 'м²'),
        ('linear_meter', 'пог. м'),
        ('piece', 'шт'),
        ('set', 'комплект')
    ]
    
    # Источники лидов
    LEAD_SOURCES = [
        ('website', 'Сайт'),
        ('social_media', 'Социальные сети'),
        ('referral', 'Рекомендация'),
        ('advertising', 'Реклама'),
        ('exhibition', 'Выставка'),
        ('phone', 'Телефонный звонок'),
        ('other', 'Другое')
    ]
