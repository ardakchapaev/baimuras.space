
"""
Middleware безопасности для BaiMuras Platform
Дополнительные слои защиты для продакшн среды
"""

import time
import logging
from functools import wraps
from flask import request, jsonify, current_app, g
from collections import defaultdict, deque
import hashlib
import hmac


logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """Middleware для дополнительной безопасности"""

    def __init__(self, app=None):
        self.app = app
        self.request_history = defaultdict(deque)
        self.blocked_ips = set()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Инициализация middleware с приложением Flask"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)

        # Настройки безопасности
        self.max_requests_per_minute = app.config.get(
            'MAX_REQUESTS_PER_MINUTE', 60)
        self.max_requests_per_hour = app.config.get(
            'MAX_REQUESTS_PER_HOUR', 1000)
        self.block_duration = app.config.get('BLOCK_DURATION_MINUTES', 15)

        logger.info("Security middleware initialized")

    def get_client_ip(self):
        """Получение реального IP клиента"""
        # Проверяем заголовки прокси
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr

    def is_suspicious_request(self):
        """Проверка на подозрительные запросы"""
        # Проверка на SQL injection паттерны
        suspicious_patterns = [
            'union select', 'drop table', 'insert into', 'delete from',
            'script>', '<iframe', 'javascript:', 'eval(', 'alert(',
            '../', '..\\', '/etc/passwd', '/proc/self'
        ]

        query_string = request.query_string.decode(
            'utf-8', errors='ignore').lower()
        user_agent = request.headers.get('User-Agent', '').lower()

        for pattern in suspicious_patterns:
            if pattern in query_string or pattern in user_agent:
                return True

        # Проверка на аномально длинные запросы
        if len(request.url) > 2048:
            return True

        # Проверка на отсутствие User-Agent (боты)
        if not request.headers.get('User-Agent'):
            return True

        return False

    def check_rate_limit(self, client_ip):
        """Проверка лимитов запросов"""
        current_time = time.time()

        # Очищаем старые записи
        minute_ago = current_time - 60
        hour_ago = current_time - 3600

        history = self.request_history[client_ip]

        # Удаляем запросы старше часа
        while history and history[0] < hour_ago:
            history.popleft()

        # Подсчитываем запросы за последнюю минуту и час
        requests_last_minute = sum(
            1 for timestamp in history if timestamp > minute_ago)
        requests_last_hour = len(history)

        # Проверяем лимиты
        if requests_last_minute > self.max_requests_per_minute:
            logger.warning(
                f"Rate limit exceeded for IP {client_ip}: {requests_last_minute} requests/minute")
            return False

        if requests_last_hour > self.max_requests_per_hour:
            logger.warning(
                f"Rate limit exceeded for IP {client_ip}: {requests_last_hour} requests/hour")
            return False

        # Добавляем текущий запрос
        history.append(current_time)

        return True

    def before_request(self):
        """Обработка запроса перед его выполнением"""
        g.request_start_time = time.time()

        client_ip = self.get_client_ip()
        g.client_ip = client_ip

        # Проверка заблокированных IP
        if client_ip in self.blocked_ips:
            logger.warning(f"Blocked IP attempted access: {client_ip}")
            return jsonify({'error': 'Access denied'}), 403

        # Проверка подозрительных запросов
        if self.is_suspicious_request():
            logger.warning(
                f"Suspicious request from {client_ip}: {request.url}")
            self.blocked_ips.add(client_ip)
            return jsonify({'error': 'Suspicious activity detected'}), 403

        # Проверка rate limiting
        if not self.check_rate_limit(client_ip):
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return jsonify({'error': 'Rate limit exceeded'}), 429

    def after_request(self, response):
        """Обработка ответа после выполнения запроса"""
        # Добавляем заголовки безопасности
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Удаляем заголовки, раскрывающие информацию о сервере
        response.headers.pop('Server', None)
        response.headers.pop('X-Powered-By', None)

        # Логирование времени выполнения запроса
        if hasattr(g, 'request_start_time'):
            duration = time.time() - g.request_start_time
            if duration > 5.0:  # Логируем медленные запросы
                logger.warning(
                    f"Slow request: {request.method} {request.path} took {duration:.2f}s")

        return response


def require_api_key(f):
    """Декоратор для проверки API ключа"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            return jsonify({'error': 'API key required'}), 401

        # Проверяем API ключ (в продакшн должен быть в базе данных)
        expected_key = current_app.config.get('API_KEY')
        if not expected_key or not hmac.compare_digest(api_key, expected_key):
            logger.warning(
                f"Invalid API key attempt from {g.get('client_ip', 'unknown')}")
            return jsonify({'error': 'Invalid API key'}), 401

        return f(*args, **kwargs)

    return decorated_function


def require_signature(f):
    """Декоратор для проверки подписи запроса"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        signature = request.headers.get('X-Signature')

        if not signature:
            return jsonify({'error': 'Signature required'}), 401

        # Получаем секретный ключ для подписи
        secret_key = current_app.config.get('WEBHOOK_SECRET_KEY')
        if not secret_key:
            logger.error("WEBHOOK_SECRET_KEY not configured")
            return jsonify({'error': 'Server configuration error'}), 500

        # Вычисляем ожидаемую подпись
        payload = request.get_data()
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        expected_signature = f"sha256={expected_signature}"

        if not hmac.compare_digest(signature, expected_signature):
            logger.warning(
                f"Invalid signature from {g.get('client_ip', 'unknown')}")
            return jsonify({'error': 'Invalid signature'}), 401

        return f(*args, **kwargs)

    return decorated_function


class RequestLogger:
    """Логгер запросов для аудита безопасности"""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Инициализация логгера с приложением Flask"""
        app.before_request(self.log_request)
        app.after_request(self.log_response)

        # Настройка отдельного логгера для аудита
        self.audit_logger = logging.getLogger('audit')
        handler = logging.FileHandler('logs/audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.audit_logger.addHandler(handler)
        self.audit_logger.setLevel(logging.INFO)

    def log_request(self):
        """Логирование входящего запроса"""
        client_ip = g.get('client_ip', request.remote_addr)
        user_agent = request.headers.get('User-Agent', 'Unknown')

        self.audit_logger.info(
            f"REQUEST - IP: {client_ip} - Method: {request.method} - "
            f"Path: {request.path} - User-Agent: {user_agent}"
        )

    def log_response(self, response):
        """Логирование ответа"""
        client_ip = g.get('client_ip', request.remote_addr)

        # Логируем ошибки и подозрительную активность
        if response.status_code >= 400:
            self.audit_logger.warning(
                f"RESPONSE - IP: {client_ip} - Status: {response.status_code} - "
                f"Path: {request.path}")

        return response
