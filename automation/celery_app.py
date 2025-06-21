
"""Конфигурация Celery для автоматизации BaiMuras."""

import os
from celery import Celery
from kombu import Queue


def make_celery(app_name=__name__):
    """Создание экземпляра Celery."""

    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    celery = Celery(
        app_name,
        broker=redis_url,
        backend=redis_url,
        include=[
            'automation.tasks.email_tasks',
            'automation.tasks.notification_tasks',
            'automation.tasks.backup_tasks',
            'automation.tasks.analytics_tasks'
        ]
    )

    # Конфигурация Celery
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Bishkek',
        enable_utc=True,

        # Настройки задач
        task_always_eager=False,
        task_eager_propagates=True,
        task_ignore_result=False,
        result_expires=3600,

        # Маршрутизация задач
        task_routes={
            'automation.tasks.email_tasks.*': {'queue': 'email'},
            'automation.tasks.notification_tasks.*': {'queue': 'notifications'},
            'automation.tasks.backup_tasks.*': {'queue': 'maintenance'},
            'automation.tasks.analytics_tasks.*': {'queue': 'analytics'},
        },

        # Очереди
        task_default_queue='default',
        task_queues=(
            Queue('default'),
            Queue('email'),
            Queue('notifications'),
            Queue('maintenance'),
            Queue('analytics'),
        ),

        # Настройки воркера
        worker_prefetch_multiplier=4,
        worker_max_tasks_per_child=1000,

        # Beat schedule для периодических задач
        beat_schedule={
            'daily-backup': {
                'task': 'automation.tasks.backup_tasks.daily_database_backup',
                'schedule': 86400.0,  # каждые 24 часа
            },
            'weekly-analytics': {
                'task': 'automation.tasks.analytics_tasks.generate_weekly_report',
                'schedule': 604800.0,  # каждую неделю
            },
            'check-overdue-measurements': {
                'task': 'automation.tasks.notification_tasks.check_overdue_measurements',
                'schedule': 3600.0,  # каждый час
            },
        },
    )

    return celery


# Создание экземпляра Celery
celery_app = make_celery()

if __name__ == '__main__':
    celery_app.start()
