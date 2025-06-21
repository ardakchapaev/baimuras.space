
"""Main application module for BaiMuras Platform.

This module creates and configures the Flask application with security enhancements,
proper error handling, and CORS policies using the new SecretManager system.
"""

from src.errors import register_error_handlers  # pylint: disable=wrong-import-position
from src.content import NAVIGATION, FOOTER  # pylint: disable=wrong-import-position
from src.utils import get_current_language, get_app_version  # pylint: disable=wrong-import-position
from src.security_middleware import SecurityMiddleware, RequestLogger  # pylint: disable=wrong-import-position
from src.health_check import health_bp  # pylint: disable=wrong-import-position
from src.routes.webhooks import webhooks_bp  # pylint: disable=wrong-import-position
from src.routes.crm import crm_bp  # pylint: disable=wrong-import-position
from src.routes.user import user_bp  # pylint: disable=wrong-import-position
from src.routes.main_routes import main_bp  # pylint: disable=wrong-import-position
from src.routes.api_v1 import api_v1_bp  # pylint: disable=wrong-import-position
from src.routes.api import api_bp  # pylint: disable=wrong-import-position
from src.models import db  # pylint: disable=wrong-import-position
from src.config_secure import get_config  # pylint: disable=wrong-import-position
from flask_limiter.util import get_remote_address  # pylint: disable=wrong-import-position
from flask_limiter import Limiter  # pylint: disable=wrong-import-position
from flask_talisman import Talisman  # pylint: disable=wrong-import-position
from flask_wtf.csrf import CSRFProtect  # pylint: disable=wrong-import-position
from flask_cors import CORS  # pylint: disable=wrong-import-position
from flask import Flask, send_from_directory, session  # pylint: disable=wrong-import-position
import datetime
import logging
import os
from src.utils.logging_config import logger
import sys
import time
from typing import Dict, Any

# НЕ МЕНЯТЬ !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name: str = None) -> Flask:
    """Create and configure Flask application with SecretManager.

    Args:
        config_name: Configuration environment name

    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    application = Flask(__name__)

    # Устанавливаем время запуска для мониторинга
    application.start_time = time.time()

    # Load secure configuration with SecretManager
    try:
        config_obj = get_config(config_name)

        # Применяем конфигурацию к приложению
        for key, value in vars(config_obj).items():
            if not key.startswith(
                    '_') and key != 'secret_manager' and key != 'logger':
                application.config[key] = value

        # Сохраняем ссылку на secret_manager для использования в приложении
        application.config['secret_manager'] = config_obj.secret_manager
        application.config['environment'] = config_obj.environment

        logger.info(
            f"Configuration loaded successfully for environment: {config_name}")

    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise RuntimeError(f"Configuration loading failed: {e}") from e

    # Initialize extensions
    try:
        db.init_app(application)
        logger.info("Database initialized successfully")

        # Initialize security middleware
        SecurityMiddleware(application)
        RequestLogger(application)
        logger.info("Security middleware initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize extensions: {e}")
        raise RuntimeError(f"Extension initialization failed: {e}") from e

    # Rate limiting with Redis backend
    limiter = Limiter(
        get_remote_address,
        app=application,
        storage_uri=application.config.get('RATELIMIT_STORAGE_URL'),
        default_limits=[
            application.config.get(
                'RATELIMIT_DEFAULT',
                '100 per hour')])

    # CSRF Protection (disabled in development for API testing)
    if not application.config.get('DEBUG', False):
        CSRFProtect(application)

    # CORS Configuration
    cors_origins = ["https://baimuras.space", "https://www.baimuras.space"]
    if application.config.get('DEBUG', False):
        cors_origins.extend(
            ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"])

    CORS(application,
         resources={r"/api/*": {"origins": cors_origins,
                                "methods": ["GET",
                                            "POST",
                                            "PUT",
                                            "DELETE",
                                            "OPTIONS"],
                                "allow_headers": ["Content-Type",
                                                  "Authorization",
                                                  "X-CSRFToken",
                                                  "X-API-Key"],
                                "supports_credentials": True}})

    # Security Headers with Talisman
    talisman_config = application.config.get('TALISMAN_CONFIG', {})
    if not talisman_config:
        # Default CSP for development/production
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

        force_https = not application.config.get('DEBUG', False)
        Talisman(
            application,
            content_security_policy=csp,
            force_https=force_https)
    else:
        Talisman(application, **talisman_config)

    # Configure logging
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
        application.logger.info('BaiMuras startup')

    # Register blueprints
    application.register_blueprint(main_bp)
    application.register_blueprint(api_bp)
    application.register_blueprint(api_v1_bp)
    application.register_blueprint(user_bp)
    application.register_blueprint(crm_bp)
    application.register_blueprint(webhooks_bp)
    application.register_blueprint(health_bp)  # Health check endpoints

    # Context processors
    @application.context_processor
    def inject_global_vars() -> Dict[str, Any]:
        """Inject global variables into templates."""
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
        """Execute before each request."""
        try:
            session.permanent = True
            application.permanent_session_lifetime = datetime.timedelta(
                hours=24)
        except (KeyError, ValueError, TypeError) as request_error:
            application.logger.warning(
                'Session setup error: %s', str(request_error))

    @application.after_request
    def after_request(response):
        """Execute after each request."""
        try:
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            return response
        except (KeyError, ValueError, AttributeError) as response_error:
            application.logger.warning(
                'Response header error: %s', str(response_error))
            return response

    @application.route('/favicon.ico')
    def favicon():
        """Serve favicon."""
        try:
            return send_from_directory(
                os.path.join(application.root_path, 'static', 'images'),
                'favicon.ico',
                mimetype='image/vnd.microsoft.icon'
            )
        except (FileNotFoundError, OSError, IOError) as favicon_error:
            application.logger.warning('Favicon error: %s', str(favicon_error))
            return '', 404

    # Register error handlers
    register_error_handlers(application)

    # Create database tables
    with application.app_context():
        try:
            db.create_all()
            application.logger.info('Database tables created successfully')
        except (OSError, IOError, RuntimeError) as db_error:
            application.logger.error(
                'Database creation error: %s', str(db_error))

    return application


# Create application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=8000, debug=debug_mode)
