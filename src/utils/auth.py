
"""
Утилиты для аутентификации и авторизации
"""
from functools import wraps
from flask import session, redirect, url_for, request, flash


def login_required(f):
    """
    Декоратор для проверки аутентификации пользователя
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """decorated_function функция."""
        if 'user_id' not in session:
            flash('Необходимо войти в систему', 'warning')
            return redirect(url_for('main.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Декоратор для проверки прав администратора
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """decorated_function функция."""
        if 'user_id' not in session:
            flash('Недостаточно прав доступа', 'error')
            return redirect(url_for('main.index'))
        # Здесь можно добавить проверку роли администратора из БД
        return f(*args, **kwargs)
    return decorated_function
