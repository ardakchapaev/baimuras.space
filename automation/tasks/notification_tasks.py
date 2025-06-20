
"""Задачи для уведомлений и напоминаний."""

from datetime import datetime, timedelta
from automation.celery_app import celery_app
from automation.tasks.email_tasks import send_measurement_reminder, send_project_status_update

@celery_app.task
def check_overdue_measurements():
    """Проверка просроченных замеров."""
    try:
        # В реальном приложении здесь будет запрос к БД
        # from src.models.updated_models import Measurement
        # overdue_measurements = Measurement.query.filter(
        #     Measurement.scheduled_date < datetime.now(),
        #     Measurement.status == 'scheduled'
        # ).all()
        
        # Заглушка для демонстрации
        print("Checking for overdue measurements...")
        
        # Здесь можно отправить уведомления менеджерам
        return {'status': 'success', 'checked_measurements': 0}
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@celery_app.task
def send_daily_measurement_reminders():
    """Отправка ежедневных напоминаний о замерах."""
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        
        # В реальном приложении запрос к БД
        # measurements_tomorrow = Measurement.query.filter(
        #     Measurement.scheduled_date.between(
        #         tomorrow.replace(hour=0, minute=0, second=0),
        #         tomorrow.replace(hour=23, minute=59, second=59)
        #     ),
        #     Measurement.status == 'scheduled'
        # ).all()
        
        # Заглушка
        measurements_count = 0
        
        # for measurement in measurements_tomorrow:
        #     send_measurement_reminder.delay(measurement.id)
        #     measurements_count += 1
        
        return {
            'status': 'success', 
            'reminders_sent': measurements_count
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@celery_app.task
def notify_lead_assignment(lead_id: int, manager_id: int):
    """Уведомление о назначении лида менеджеру."""
    try:
        # Уведомление менеджеру о новом лиде
        subject = "Новый лид назначен вам"
        message = f"Вам назначен новый лид #{lead_id}. Пожалуйста, свяжитесь с клиентом."
        
        # В реальном приложении получение email менеджера из БД
        # manager = User.query.get(manager_id)
        # send_email(manager.email, subject, message)
        
        print(f"Lead {lead_id} assigned to manager {manager_id}")
        
        return {'status': 'success', 'lead_id': lead_id}
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@celery_app.task
def project_milestone_notification(project_id: int, milestone: str):
    """Уведомление о достижении важной вехи проекта."""
    try:
        milestone_messages = {
            'design_approved': 'Дизайн-проект утвержден клиентом',
            'production_started': 'Производство мебели начато',
            'production_completed': 'Производство мебели завершено',
            'installation_scheduled': 'Запланирована установка мебели',
            'project_completed': 'Проект успешно завершен'
        }
        
        message = milestone_messages.get(milestone, f'Проект обновлен: {milestone}')
        
        # Отправка уведомления клиенту и команде
        send_project_status_update.delay(project_id, milestone)
        
        print(f"Project {project_id} milestone: {message}")
        
        return {
            'status': 'success', 
            'project_id': project_id, 
            'milestone': milestone
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@celery_app.task
def send_weekly_digest():
    """Отправка еженедельного дайджеста команде."""
    try:
        # Собираем статистику за неделю
        week_ago = datetime.now() - timedelta(days=7)
        
        # В реальном приложении запросы к БД
        stats = {
            'new_leads': 0,  # Lead.query.filter(Lead.created_at >= week_ago).count()
            'new_projects': 0,  # Project.query.filter(Project.created_at >= week_ago).count()
            'completed_projects': 0,  # Project.query.filter(Project.status == 'completed', Project.updated_at >= week_ago).count()
            'measurements_scheduled': 0  # Measurement.query.filter(Measurement.scheduled_date >= datetime.now()).count()
        }
        
        print(f"Weekly digest prepared: {stats}")
        
        return {'status': 'success', 'stats': stats}
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
