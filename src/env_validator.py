"""
Модуль для валидации обязательных переменных окружения
"""
import os
import sys
from typing import List, Optional


class EnvironmentValidator:
    """Класс для валидации переменных окружения"""

    REQUIRED_VARS = [
        "SECRET_KEY",
        "JWT_SECRET_KEY",
    ]

    PRODUCTION_REQUIRED_VARS = [
        "DATABASE_URL",
        "REDIS_URL",
        "MAIL_SERVER",
        "MAIL_USERNAME",
        "MAIL_PASSWORD",
    ]

    @classmethod
    def validate_environment(cls, environment: str = "development") -> bool:
        """
        Валидация переменных окружения
        
        Args:
            environment: Окружение (development, staging, production)
            
        Returns:
            bool: True если все переменные установлены
            
        Raises:
            SystemExit: Если обязательные переменные не установлены
        """
        missing_vars = cls._get_missing_vars(environment)
        
        if missing_vars:
            cls._print_missing_vars_error(missing_vars, environment)
            sys.exit(1)
            
        cls._validate_secret_keys()
        return True

    @classmethod
    def _get_missing_vars(cls, environment: str) -> List[str]:
        """Получить список отсутствующих переменных"""
        missing = []
        
        # Проверяем базовые переменные
        for var in cls.REQUIRED_VARS:
            if not os.getenv(var):
                missing.append(var)
        
        # Для продакшена проверяем дополнительные переменные
        if environment == "production":
            for var in cls.PRODUCTION_REQUIRED_VARS:
                if not os.getenv(var):
                    missing.append(var)
                    
        return missing

    @classmethod
    def _validate_secret_keys(cls) -> None:
        """Валидация секретных ключей"""
        secret_key = os.getenv("SECRET_KEY", "")
        jwt_secret = os.getenv("JWT_SECRET_KEY", "")
        
        if len(secret_key) < 32:
            print("ERROR: SECRET_KEY должен быть длиной минимум 32 символа")
            sys.exit(1)
            
        if len(jwt_secret) < 32:
            print("ERROR: JWT_SECRET_KEY должен быть длиной минимум 32 символа")
            sys.exit(1)

    @classmethod
    def _print_missing_vars_error(cls, missing_vars: List[str], environment: str) -> None:
        """Вывод ошибки о недостающих переменных"""
        print("=" * 60)
        print("ОШИБКА: Отсутствуют обязательные переменные окружения!")
        print("=" * 60)
        print(f"Окружение: {environment}")
        print("Отсутствующие переменные:")
        for var in missing_vars:
            print(f"  - {var}")
        print()
        print("Решение:")
        print("1. Скопируйте .env.example в .env")
        print("2. Заполните все обязательные переменные")
        print("3. Перезапустите приложение")
        print("=" * 60)


def validate_required_env_vars(environment: Optional[str] = None) -> bool:
    """
    Функция-обертка для валидации переменных окружения
    
    Args:
        environment: Окружение для валидации
        
    Returns:
        bool: True если валидация прошла успешно
    """
    if environment is None:
        environment = os.getenv("FLASK_ENV", "development")
        
    return EnvironmentValidator.validate_environment(environment)
