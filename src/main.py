
import os
import sys
import datetime
from flask import Flask, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

# НЕ МЕНЯТЬ !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.routes.main_routes import main_bp
from src.routes.user import user_bp
from src.routes.api import api_bp
from src.models.user import db
from src.config import Config

def create_app():
    app = Flask(__name__, 
                static_folder=os.path.join(os.path.dirname(__file__), 'static'), 
                template_folder='templates')
    
    # Загружаем конфигурацию
    app.config.from_object(Config)
    
    # Инициализируем расширения
    db.init_app(app)
    csrf = CSRFProtect(app)
    
    # Настраиваем CORS для API
    CORS(app, resources={
        r"/api/*": {
            "origins": ["https://hub.baimuras.space", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Регистрируем блюпринты
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Исключаем API endpoints от CSRF защиты
    csrf.exempt(api_bp)
    
    # Создаем таблицы базы данных
    with app.app_context():
        db.create_all()
    
    # Делаем session и current_year доступными во всех шаблонах
    @app.context_processor
    def inject_global_vars():
        return dict(session=session, current_year=datetime.datetime.utcnow().year)
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)
    
    @app.route("/health")
    def health_check():
        return "OK", 200
    
    # Обработчики ошибок
    from src.errors import register_error_handlers
    register_error_handlers(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
