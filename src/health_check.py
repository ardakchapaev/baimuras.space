"""
Health Check система для BaiMuras Platform
Предоставляет эндпоинты для мониторинга состояния приложения
"""

import logging
import time
from datetime import datetime

import psutil
from flask import Blueprint, current_app, jsonify
from sqlalchemy import text

from src.models import db
from src.secret_manager import SecretManager

health_bp = Blueprint("health", __name__, url_prefix="/health")
logger = logging.getLogger(__name__)


@health_bp.route("/")
def health_check():
    """Базовая проверка здоровья приложения"""
    try:
        return (
            jsonify(
                {
                    "status": "healthy",
                    "timestamp": datetime.utcnow().isoformat(),
                    "service": "BaiMuras Platform",
                    "version": "1.0.0",
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            500,
        )


@health_bp.route("/detailed")
def detailed_health_check():
    """Детальная проверка здоровья всех компонентов"""
    start_time = time.time()
    checks = {}
    overall_status = "healthy"

    # Проверка базы данных
    try:
        db.session.execute(text("SELECT 1"))
        checks["database"] = {
            "status": "healthy",
            "message": "Database connection successful",
        }
    except Exception as e:
        checks["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
        }
        overall_status = "unhealthy"

    # Проверка Redis (если используется)
    try:
        import redis

        redis_url = current_app.config.get(
            "CELERY_BROKER_URL", "redis://localhost:6379/0"
        )
        r = redis.from_url(redis_url)
        r.ping()
        checks["redis"] = {
            "status": "healthy",
            "message": "Redis connection successful",
        }
    except Exception as e:
        checks["redis"] = {
            "status": "unhealthy",
            "message": f"Redis connection failed: {str(e)}",
        }
        overall_status = "degraded" if overall_status == "healthy" else "unhealthy"

    # Проверка системных ресурсов
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        cpu_percent = psutil.cpu_percent(interval=1)

        checks["system"] = {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_free_gb": round(disk.free / (1024**3), 2),
        }

        # Предупреждения о высоком использовании ресурсов
        if memory.percent > 90 or disk.percent > 90 or cpu_percent > 90:
            checks["system"]["status"] = "warning"
            checks["system"]["message"] = "High resource usage detected"
            overall_status = (
                "degraded" if overall_status == "healthy" else overall_status
            )

    except Exception as e:
        checks["system"] = {
            "status": "unhealthy",
            "message": f"System check failed: {str(e)}",
        }
        overall_status = "degraded" if overall_status == "healthy" else "unhealthy"

    # Проверка конфигурации
    try:
        secret_manager = getattr(current_app.config, "secret_manager", None)
        if secret_manager and isinstance(secret_manager, SecretManager):
            checks["configuration"] = {
                "status": "healthy",
                "message": "Configuration loaded successfully",
                "environment": current_app.config.get("environment", "unknown"),
            }
        else:
            checks["configuration"] = {
                "status": "warning",
                "message": "SecretManager not found or not properly initialized",
            }
            overall_status = (
                "degraded" if overall_status == "healthy" else overall_status
            )
    except Exception as e:
        checks["configuration"] = {
            "status": "unhealthy",
            "message": f"Configuration check failed: {str(e)}",
        }
        overall_status = "degraded" if overall_status == "healthy" else "unhealthy"

    response_time = round((time.time() - start_time) * 1000, 2)

    response = {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "service": "BaiMuras Platform",
        "version": "1.0.0",
        "response_time_ms": response_time,
        "checks": checks,
    }

    status_code = (
        200
        if overall_status == "healthy"
        else (206 if overall_status == "degraded" else 500)
    )
    return jsonify(response), status_code


@health_bp.route("/ready")
def readiness_check():
    """Проверка готовности приложения к обслуживанию запросов"""
    try:
        # Проверяем критически важные компоненты
        db.session.execute(text("SELECT 1"))

        return (
            jsonify(
                {
                    "status": "ready",
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": "Application is ready to serve requests",
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return (
            jsonify(
                {
                    "status": "not_ready",
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": str(e),
                }
            ),
            503,
        )


@health_bp.route("/live")
def liveness_check():
    """Проверка жизнеспособности приложения"""
    try:
        # Простая проверка, что приложение отвечает
        return (
            jsonify(
                {
                    "status": "alive",
                    "timestamp": datetime.utcnow().isoformat(),
                    "uptime_seconds": time.time()
                    - getattr(current_app, "start_time", time.time()),
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Liveness check failed: {e}")
        return (
            jsonify(
                {
                    "status": "dead",
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": str(e),
                }
            ),
            500,
        )


@health_bp.route("/metrics")
def metrics():
    """Базовые метрики приложения"""
    try:
        # Системные метрики
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        cpu_percent = psutil.cpu_percent(interval=0.1)

        # Метрики базы данных
        try:
            result = db.session.execute(
                text(
                    """
                SELECT
                    (SELECT COUNT(*) FROM user) as user_count,
                    (SELECT COUNT(*) FROM project) as project_count,
                    (SELECT COUNT(*) FROM lead) as lead_count,
                    (SELECT COUNT(*) FROM consultation) as consultation_count
            """
                )
            )
            row = result.fetchone()
            db_metrics = {
                "users": row[0] if row else 0,
                "projects": row[1] if row else 0,
                "leads": row[2] if row else 0,
                "consultations": row[3] if row else 0,
            }
        except Exception as e:
            logger.warning(f"Could not fetch database metrics: {e}")
            db_metrics = {"error": "Database metrics unavailable"}

        return (
            jsonify(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "system": {
                        "cpu_percent": cpu_percent,
                        "memory_percent": memory.percent,
                        "memory_used_gb": round(
                            (memory.total - memory.available) / (1024**3), 2
                        ),
                        "memory_total_gb": round(memory.total / (1024**3), 2),
                        "disk_percent": disk.percent,
                        "disk_used_gb": round(disk.used / (1024**3), 2),
                        "disk_total_gb": round(disk.total / (1024**3), 2),
                    },
                    "database": db_metrics,
                    "application": {
                        "environment": current_app.config.get("environment", "unknown"),
                        "debug": current_app.debug,
                        "testing": current_app.testing,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Metrics collection failed: {e}")
        return (
            jsonify(
                {
                    "error": "Metrics collection failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            500,
        )
