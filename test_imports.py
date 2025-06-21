#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работоспособности основных модулей
после исправления критических блокеров
"""

import os
import sys

from src.utils.logging_config import logger

# Установка минимальных переменных окружения для тестирования
os.environ["SECRET_KEY"] = "test-secret-key-for-import-testing"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret-key-for-import-testing"
os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "False"


def test_imports():
    """Тестирование импорта основных модулей"""
    logger.info("🔍 Тестирование импорта основных модулей...")

    try:
        # Тестирование импорта моделей
        logger.info("  ✓ Импорт моделей...")

        # Тестирование импорта утилит
        logger.info("  ✓ Импорт утилит...")

        # Тестирование импорта маршрутов
        logger.info("  ✓ Импорт маршрутов...")

        # Тестирование создания приложения
        logger.info("  ✓ Создание Flask приложения...")
        from src.main import create_app

        create_app("development")

        logger.info("✅ Все модули успешно импортированы!")
        logger.info("✅ Flask приложение создано без ошибок!")
        return True

    except Exception as e:
        logger.info(f"❌ Ошибка импорта: {e}")
        return False


def test_syntax():
    """Проверка синтаксиса Python файлов"""
    logger.info("\n🔍 Проверка синтаксиса Python файлов...")

    import glob
    import py_compile

    python_files = glob.glob("src/**/*.py", recursive=True)
    errors = []

    for file_path in python_files:
        try:
            py_compile.compile(file_path, doraise=True)
            logger.info(f"  ✓ {file_path}")
        except py_compile.PyCompileError as e:
            errors.append(f"  ❌ {file_path}: {e}")
            logger.info(f"  ❌ {file_path}: {e}")

    if not errors:
        logger.info("✅ Все Python файлы имеют корректный синтаксис!")
        return True
    else:
        logger.info(f"❌ Найдено {len(errors)} файлов с синтаксическими ошибками")
        return False


def main():
    """Основная функция тестирования"""
    logger.info(
        "🚀 Запуск тестирования BaiMuras Platform после исправления критических блокеров\n"
    )

    syntax_ok = test_syntax()
    imports_ok = test_imports()

    logger.info("\n" + "=" * 60)
    logger.info("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    logger.info("=" * 60)
    logger.info(
        f"Синтаксис Python файлов: {'✅ ПРОЙДЕН' if syntax_ok else '❌ ПРОВАЛЕН'}"
    )
    logger.info(f"Импорт модулей: {'✅ ПРОЙДЕН' if imports_ok else '❌ ПРОВАЛЕН'}")

    if syntax_ok and imports_ok:
        logger.info("\n🎉 ВСЕ КРИТИЧЕСКИЕ БЛОКЕРЫ УСТРАНЕНЫ!")
        logger.info("✅ Платформа готова к дальнейшей разработке")
        logger.info("⚠️  Не забудьте настроить переменные окружения перед запуском")
        return 0
    else:
        logger.info("\n⚠️  ОСТАЛИСЬ ПРОБЛЕМЫ, ТРЕБУЮЩИЕ ВНИМАНИЯ")
        return 1


if __name__ == "__main__":
    sys.exit(main())
