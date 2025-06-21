"""
JWT утилиты для API аутентификации
"""

import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, Optional

import jwt
from flask import current_app, g, jsonify, request

from ..models import User


class JWTManager:
    """Менеджер для работы с JWT токенами"""

    def __init__(self, app=None):
        """__init__ функция."""
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Инициализация с Flask приложением"""
        jwt_secret = os.environ.get("JWT_SECRET_KEY")
        if not jwt_secret:
            raise ValueError("No JWT_SECRET_KEY set in environment variables")
        app.config.setdefault("JWT_SECRET_KEY", jwt_secret)
        app.config.setdefault("JWT_ACCESS_TOKEN_EXPIRES", timedelta(hours=1))
        app.config.setdefault("JWT_REFRESH_TOKEN_EXPIRES", timedelta(days=30))
        app.config.setdefault("JWT_ALGORITHM", "HS256")

        # Сохранение экземпляра в app
        app.extensions = getattr(app, "extensions", {})
        app.extensions["jwt"] = self


def generate_tokens(
    user_id: int, user_email: str, user_role: str = "user"
) -> Dict[str, str]:
    """
    Генерация access и refresh токенов

    Args:
        user_id: ID пользователя
        user_email: Email пользователя
        user_role: Роль пользователя

    Returns:
        Dict с access_token и refresh_token
    """
    secret_key = current_app.config["JWT_SECRET_KEY"]
    algorithm = current_app.config["JWT_ALGORITHM"]

    # Access token (короткий срок жизни)
    access_payload = {
        "user_id": user_id,
        "email": user_email,
        "role": user_role,
        "type": "access",
        "exp": datetime.utcnow() + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        "iat": datetime.utcnow(),
    }

    # Refresh token (длинный срок жизни)
    refresh_payload = {
        "user_id": user_id,
        "email": user_email,
        "type": "refresh",
        "exp": datetime.utcnow() + current_app.config["JWT_REFRESH_TOKEN_EXPIRES"],
        "iat": datetime.utcnow(),
    }

    access_token = jwt.encode(access_payload, secret_key, algorithm=algorithm)
    refresh_token = jwt.encode(refresh_payload, secret_key, algorithm=algorithm)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": int(
            current_app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds()
        ),
    }


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Декодирование JWT токена

    Args:
        token: JWT токен

    Returns:
        Payload токена или None при ошибке
    """
    try:
        secret_key = current_app.config["JWT_SECRET_KEY"]
        algorithm = current_app.config["JWT_ALGORITHM"]

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload

    except jwt.ExpiredSignatureError:
        current_app.logger.warning("JWT token expired")
        return None
    except jwt.InvalidTokenError as e:
        current_app.logger.warning(f"Invalid JWT token: {str(e)}")
        return None
    except Exception as e:
        current_app.logger.error(f"JWT decode error: {str(e)}")
        return None


def refresh_access_token(refresh_token: str) -> Optional[Dict[str, str]]:
    """
    Обновление access токена с помощью refresh токена

    Args:
        refresh_token: Refresh токен

    Returns:
        Новые токены или None при ошибке
    """
    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        return None

    # Проверка существования пользователя
    user = User.query.get(payload.get("user_id"))
    if not user:
        return None

    # Генерация новых токенов
    return generate_tokens(user.id, user.email, user.role.name if user.role else "user")


def get_current_user() -> Optional[User]:
    """
    Получение текущего пользователя из JWT токена

    Returns:
        Объект пользователя или None
    """
    if hasattr(g, "current_user"):
        return g.current_user

    return None


def jwt_required(f: Callable) -> Callable:
    """
    Декоратор для защиты endpoints с помощью JWT

    Args:
        f: Функция для защиты

    Returns:
        Защищенная функция
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        """decorated_function функция."""
        token = None

        # Получение токена из заголовка Authorization
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({"error": "Invalid authorization header format"}), 401

        # Получение токена из параметров запроса (fallback)
        if not token:
            token = request.args.get("token")

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        # Декодирование токена
        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Token is invalid or expired"}), 401

        # Проверка типа токена
        if payload.get("type") != "access":
            return jsonify({"error": "Invalid token type"}), 401

        # Получение пользователя
        user = User.query.get(payload.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 401

        # Сохранение пользователя в контексте
        g.current_user = user
        g.token_payload = payload

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f: Callable) -> Callable:
    """
    Декоратор для защиты endpoints, требующих права администратора

    Args:
        f: Функция для защиты

    Returns:
        Защищенная функция
    """

    @wraps(f)
    @jwt_required
    def decorated_function(*args, **kwargs):
        """decorated_function функция."""
        user = get_current_user()

        if not user or not user.role or user.role.name != "admin":
            return jsonify({"error": "Admin privileges required"}), 403

        return f(*args, **kwargs)

    return decorated_function


def manager_required(f: Callable) -> Callable:
    """
    Декоратор для защиты endpoints, требующих права менеджера или выше

    Args:
        f: Функция для защиты

    Returns:
        Защищенная функция
    """

    @wraps(f)
    @jwt_required
    def decorated_function(*args, **kwargs):
        """decorated_function функция."""
        user = get_current_user()

        if not user or not user.role:
            return jsonify({"error": "Insufficient privileges"}), 403

        allowed_roles = ["admin", "manager"]
        if user.role.name not in allowed_roles:
            return jsonify({"error": "Manager privileges required"}), 403

        return f(*args, **kwargs)

    return decorated_function


def optional_jwt(f: Callable) -> Callable:
    """
    Декоратор для endpoints с опциональной JWT аутентификацией

    Args:
        f: Функция

    Returns:
        Функция с опциональной аутентификацией
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Получение токена из заголовка Authorization
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                pass

        # Получение токена из параметров запроса (fallback)
        if not token:
            token = request.args.get("token")

        if token:
            # Попытка декодирования токена
            payload = decode_token(token)
            if payload and payload.get("type") == "access":
                user = User.query.get(payload.get("user_id"))
                if user:
                    g.current_user = user
                    g.token_payload = payload

        # Если токена нет или он невалидный, продолжаем без аутентификации
        if not hasattr(g, "current_user"):
            g.current_user = None
            g.token_payload = None

        return f(*args, **kwargs)

    return decorated_function


def create_api_key(user_id: int, name: str, expires_days: int = 365) -> str:
    """
    Создание API ключа для пользователя

    Args:
        user_id: ID пользователя
        name: Название API ключа
        expires_days: Срок действия в днях

    Returns:
        API ключ
    """
    secret_key = current_app.config["JWT_SECRET_KEY"]
    algorithm = current_app.config["JWT_ALGORITHM"]

    payload = {
        "user_id": user_id,
        "type": "api_key",
        "name": name,
        "exp": datetime.utcnow() + timedelta(days=expires_days),
        "iat": datetime.utcnow(),
    }

    api_key = jwt.encode(payload, secret_key, algorithm=algorithm)
    return api_key


def api_key_required(f: Callable) -> Callable:
    """
    Декоратор для защиты endpoints с помощью API ключа

    Args:
        f: Функция для защиты

    Returns:
        Защищенная функция
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = None

        # Получение API ключа из заголовка
        api_key = request.headers.get("X-API-Key")

        # Получение из параметров запроса (fallback)
        if not api_key:
            api_key = request.args.get("api_key")

        if not api_key:
            return jsonify({"error": "API key is missing"}), 401

        # Декодирование API ключа
        payload = decode_token(api_key)
        if not payload:
            return jsonify({"error": "API key is invalid or expired"}), 401

        # Проверка типа токена
        if payload.get("type") != "api_key":
            return jsonify({"error": "Invalid API key type"}), 401

        # Получение пользователя
        user = User.query.get(payload.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 401

        # Сохранение пользователя в контексте
        g.current_user = user
        g.api_key_payload = payload

        return f(*args, **kwargs)

    return decorated_function


def get_token_info() -> Dict[str, Any]:
    """
    Получение информации о текущем токене

    Returns:
        Информация о токене
    """
    if hasattr(g, "token_payload") and g.token_payload:
        return {
            "type": g.token_payload.get("type"),
            "user_id": g.token_payload.get("user_id"),
            "email": g.token_payload.get("email"),
            "role": g.token_payload.get("role"),
            "expires": g.token_payload.get("exp"),
            "issued_at": g.token_payload.get("iat"),
        }
    elif hasattr(g, "api_key_payload") and g.api_key_payload:
        return {
            "type": g.api_key_payload.get("type"),
            "user_id": g.api_key_payload.get("user_id"),
            "name": g.api_key_payload.get("name"),
            "expires": g.api_key_payload.get("exp"),
            "issued_at": g.api_key_payload.get("iat"),
        }

    return {}


# Инициализация JWT менеджера
jwt_manager = JWTManager()
