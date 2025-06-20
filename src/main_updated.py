
"""Модернизированное главное приложение BaiMuras Platform.

Обновленная версия с Flask-Migrate, полной админ-панелью и автоматизацией.
"""

import datetime
import logging
import os
import sys
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_admin import Admin

from src.config import Config, config
from src.models import db, User
from src.routes.api import api_bp
from src.routes.main_routes import main_bp
from src.routes.user import user_bp
from src.routes.crm import crm_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.utils import get_current_language, get_app_version
from src.content import NAVIGATION, FOOTER
from src.errors import register_error_handlers

# Инициализация расширений
mail = Mail()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name: str = 'default') -> Flask:
    """Создание и конфигурация Flask приложения."""
    application = Flask(__name__)
    
    # Загрузка конфигурации
    application.config.from_object(config[config_name])
    config[config_name].init_app(application)
    
    # Инициализация расширений
    db.init_app(application)
    migrate.init_app(application, db)
    mail.init_app(application)
    
    # Настройка Flask-Login
    login_manager.init_app(application)
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Rate limiting
    Limiter(
        get_remote_address,
        app=application,
        default_limits=[application.config.get('RATELIMIT_DEFAULT', '1000 per hour')]
    )
    
    # CSRF Protection
    csrf = CSRFProtect(application)
    
    # CORS Configuration
    CORS(application, resources={
        r"/api/*": {
            "origins": ["https://baimuras.space", "https://www.baimuras.space"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization", "X-CSRFToken"]
        }
    })
    
    # Настройка админ-панели
    admin = Admin(
        application, 
        name='BaiMuras Admin', 
        template_mode='bootstrap4',
        url='/admin'
    )
    
    # Security Headers с Talisman
    csp = {
        'default-src': "'self'",
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://www.google.com",
            "https://www.gstatic.com"
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://fonts.googleapis.com"
        ],
        'font-src': [
            "'self'",
            "https://fonts.gstatic.com",
            "https://cdnjs.cloudflare.com"
        ],
        'img-src': [
            "'self'",
            "data:",
            "https:",
            "http:"
        ],
        'connect-src': "'self'"
    }
    
    Talisman(application, content_security_policy=csp, force_https=False)
    
    # Настройка логирования
    if not application.debug and not application.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler('logs/baimuras.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        application.logger.addHandler(file_handler)
        application.logger.setLevel(logging.INFO)
        application.logger.info('BaiMuras Platform startup')
    
    # Регистрация blueprint'ов
    application.register_blueprint(main_bp)
    application.register_blueprint(api_bp)
    application.register_blueprint(user_bp)
    application.register_blueprint(crm_bp)
    
    # Context processors
    @application.context_processor
    def inject_global_vars() -> Dict[str, Any]:
        """Внедрение глобальных переменных в шаблоны."""
        current_lang = get_current_language()
        return {
            'current_language': current_lang,
            'languages': {'ru': 'Русский', 'ky': 'Кыргызча'},
            'navigation': NAVIGATION.get(current_lang, NAVIGATION['ru']),
            'footer_content': FOOTER.get(current_lang, FOOTER['ru']),
            'app_version': get_app_version(),
            'current_year': datetime.datetime.now().year
        }
    
    @application.before_request
    def before_request():
        """Выполнение перед каждым запросом."""
        try:
            session.permanent = True
            application.permanent_session_lifetime = datetime.timedelta(hours=24)
        except (KeyError, ValueError, TypeError) as request_error:
            application.logger.warning('Session setup error: %s', str(request_error))
    
    @application.after_request
    def after_request(response):
        """Выполнение после каждого запроса."""
        try:
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            return response
        except (KeyError, ValueError, AttributeError) as response_error:
            application.logger.warning('Response header error: %s', str(response_error))
            return response
    
    @application.route('/favicon.ico')
    def favicon():
        """Подача favicon."""
        try:
            return send_from_directory(
                os.path.join(application.root_path, 'static', 'images'),
                'favicon.ico',
                mimetype='image/vnd.microsoft.icon'
            )
        except (FileNotFoundError, OSError, IOError) as favicon_error:
            application.logger.warning('Favicon error: %s', str(favicon_error))
            return '', 404
    
    # Регистрация обработчиков ошибок
    register_error_handlers(application)
    
    # Создание таблиц БД
    with application.app_context():
        try:
            db.create_all()
            application.logger.info('Database tables created successfully')
        except (OSError, IOError, RuntimeError) as db_error:
            application.logger.error('Database creation error: %s', str(db_error))
    
    return application


# Создание экземпляра приложения
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
