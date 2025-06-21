"""
Конфигурация структурированного логирования для BaiMuras Platform
"""
import logging
import logging.config
import json
import os
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Форматтер для структурированного JSON логирования"""

    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Добавляем информацию об исключении, если есть
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        # Добавляем дополнительные поля, если есть
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'ip_address'):
            log_entry['ip_address'] = record.ip_address

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging():
    """Настройка системы логирования"""

    # Создаем директорию для логов, если не существует
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Конфигурация логирования
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': JSONFormatter,
            },
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'baimuras.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'json',
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'errors.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'json',
            },
        },
        'loggers': {
            'baimuras': {
                'handlers': ['console', 'file', 'error_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'automation': {
                'handlers': ['console', 'file', 'error_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
        }
    }

    logging.config.dictConfig(logging_config)


# Инициализируем логирование при импорте модуля
setup_logging()

# Создаем основные логгеры для использования в приложении
logger = logging.getLogger('baimuras')
automation_logger = logging.getLogger('automation')
