
"""Main application module for BaiMuras Platform.

This module creates and configures the Flask application with security enhancements,
proper error handling, and CORS policies.
"""

import datetime
import logging
import os
import sys
from typing import Dict, Any

from flask import Flask, send_from_directory, session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

# НЕ МЕНЯТЬ !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config
from src.models.user import db
from src.routes.api import api_bp
from src.routes.main_routes import main_bp
from src.routes.user import user_bp
from src.utils import get_current_language, get_app_version
from src.content import NAVIGATION, FOOTER

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create and configure Flask application with security enhancements.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        template_folder="templates",
    )

    try:
        # Загружаем конфигурацию
        app.config.from_object(Config)

        # Security headers with Talisman
        csp = {
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline' https://cdnjs.cloudflare.com",
            'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com",
            'font-src': "'self' https://fonts.gstatic.com",
            'img-src': "'self' data: https:",
            'connect-src': "'self'",
        }
        
        Talisman(
            app,
            force_https=False,  # Set to True in production
            content_security_policy=csp,
            content_security_policy_nonce_in=['script-src', 'style-src']
        )

        # Инициализируем расширения
        db.init_app(app)
        csrf = CSRFProtect(app)

        # Настраиваем CORS с безопасными политиками
        CORS(
            app,
            resources={
                r"/api/*": {
                    "origins": [
                        "https://hub.baimuras.space",
                        "http://localhost:3000",
                        "http://localhost:5000"
                    ],
                    "methods": ["GET", "POST", "PUT", "DELETE"],
                    "allow_headers": ["Content-Type", "Authorization", "X-CSRFToken"],
                    "supports_credentials": True,
                    "expose_headers": ["X-CSRFToken"]
                }
            },
            supports_credentials=True
        )

        # Регистрируем блюпринты
        app.register_blueprint(main_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(api_bp, url_prefix="/api")

        # Исключаем API endpoints от CSRF защиты
        csrf.exempt(api_bp)

        # Создаем таблицы базы данных
        with app.app_context():
            try:
                db.create_all()
                logger.info("Database tables created successfully")
            except Exception as e:
                logger.error(f"Failed to create database tables: {e}")
                raise

        # Делаем глобальные переменные доступными во всех шаблонах
        @app.context_processor
        def inject_global_vars() -> Dict[str, Any]:
            """Inject global variables into templates.
            
            Returns:
                Dict[str, Any]: Dictionary of global template variables.
            """
            try:
                current_lang = get_current_language()
                return {
                    'session': session,
                    'current_year': datetime.datetime.utcnow().year,
                    'current_language': current_lang,
                    'navigation': NAVIGATION.get(current_lang, NAVIGATION['ru']),
                    'footer_content': FOOTER.get(current_lang, FOOTER['ru']),
                    'languages': Config.LANGUAGES,
                    'app_version': get_app_version()
                }
            except Exception as e:
                logger.error(f"Error in context processor: {e}")
                return {}

        @app.route("/static/<path:filename>")
        def static_files(filename: str):
            """Serve static files securely.
            
            Args:
                filename: Path to the static file.
                
            Returns:
                Response: Static file response.
            """
            try:
                return send_from_directory(app.static_folder, filename)
            except Exception as e:
                logger.error(f"Error serving static file {filename}: {e}")
                return "File not found", 404

        @app.route("/health")
        def health_check():
            """Health check endpoint for monitoring.
            
            Returns:
                Tuple[str, int]: Health status and HTTP code.
            """
            try:
                # Basic database connectivity check
                with app.app_context():
                    db.session.execute('SELECT 1')
                return "OK", 200
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                return "Service Unavailable", 503

        # Обработчики ошибок
        from src.errors import register_error_handlers
        register_error_handlers(app)

        logger.info("Flask application created successfully")
        return app

    except Exception as e:
        logger.error(f"Failed to create Flask application: {e}")
        raise


app = create_app()

if __name__ == "__main__":
    # Production-safe configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    if debug_mode:
        logger.warning("Running in debug mode - NOT suitable for production!")
    
    app.run(host=host, port=port, debug=debug_mode)
