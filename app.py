"""
BaiMuras Platform - Главный модуль приложения
"""

import os
import sys
from pathlib import Path

# Добавляем src в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))


def create_app():
    """Создание и настройка Flask приложения"""
    try:
        from src.main import create_app as _create_app

        return _create_app()
    except ImportError:
        # Fallback для базового приложения
        from flask import Flask

        app = Flask(__name__)
        app.config["SECRET_KEY"] = os.environ.get(
            "SECRET_KEY", "dev-key-change-in-production"
        )
        return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, host="0.0.0.0", port=5000)
