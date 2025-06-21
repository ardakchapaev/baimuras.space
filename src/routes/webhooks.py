"""
Webhook endpoints для интеграции с n8n и внешними сервисами
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequest
import hmac
import hashlib
from datetime import datetime
from ..models import db, Lead, Project, ConsultationRequest
from ..utils.n8n import send_to_n8n
from ..automation.tasks.email_tasks import send_notification_email
from ..automation.tasks.notification_tasks import process_webhook_event

webhooks_bp = Blueprint('webhooks', __name__, url_prefix='/webhooks')


def verify_webhook_signature(payload, signature, secret):
    """Проверка подписи webhook для безопасности"""
    if not signature or not secret:
        return False

    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected_signature}", signature)


@webhooks_bp.route('/n8n', methods=['POST'])
def n8n_webhook():
    """
    Webhook endpoint для получения данных от n8n
    Обрабатывает различные типы событий автоматизации
    """
    try:
        # Проверка подписи если настроена
        signature = request.headers.get('X-N8N-Signature')
        webhook_secret = current_app.config.get('N8N_WEBHOOK_SECRET')

        if webhook_secret and not verify_webhook_signature(
            request.get_data(), signature, webhook_secret
        ):
            current_app.logger.warning('Invalid n8n webhook signature')
            return jsonify({'error': 'Invalid signature'}), 401

        data = request.get_json()
        if not data:
            raise BadRequest('No JSON data provided')

        event_type = data.get('event_type')
        payload = data.get('payload', {})

        current_app.logger.info(f'Received n8n webhook: {event_type}')

        # Обработка различных типов событий
        result = None

        if event_type == 'lead_processed':
            result = handle_lead_processed(payload)
        elif event_type == 'email_sent':
            result = handle_email_sent(payload)
        elif event_type == 'consultation_scheduled':
            result = handle_consultation_scheduled(payload)
        elif event_type == 'project_updated':
            result = handle_project_updated(payload)
        elif event_type == 'automation_completed':
            result = handle_automation_completed(payload)
        else:
            current_app.logger.warning(f'Unknown event type: {event_type}')
            return jsonify({'error': 'Unknown event type'}), 400

        # Асинхронная обработка события
        process_webhook_event.delay(event_type, payload)

        return jsonify({
            'status': 'success',
            'message': 'Webhook processed successfully',
            'result': result
        }), 200

    except BadRequest as e:
        current_app.logger.error(f'Bad request in n8n webhook: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f'Error processing n8n webhook: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@webhooks_bp.route('/lead-automation', methods=['POST'])
def lead_automation_webhook():
    """
    Webhook для автоматизации обработки лидов
    Принимает данные о новых лидах и запускает автоматизацию
    """
    try:
        data = request.get_json()
        lead_id = data.get('lead_id')

        if not lead_id:
            return jsonify({'error': 'lead_id is required'}), 400

        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404

        # Отправка данных в n8n для автоматизации
        automation_data = {
            'event_type': 'new_lead',
            'lead': {
                'id': lead.id,
                'name': lead.name,
                'email': lead.email,
                'phone': lead.phone,
                'service_type': lead.service_type,
                'status': lead.status,
                'created_at': lead.created_at.isoformat()
            }
        }

        # Асинхронная отправка в n8n
        send_result = send_to_n8n(automation_data)

        # Обновление статуса лида
        lead.status = 'processing'
        lead.notes = f"Автоматизация запущена: {datetime.utcnow()}"
        db.session.commit()

        current_app.logger.info(f'Lead automation started for lead {lead_id}')

        return jsonify({
            'status': 'success',
            'message': 'Lead automation started',
            'lead_id': lead_id,
            'n8n_result': send_result
        }), 200

    except Exception as e:
        current_app.logger.error(f'Error in lead automation webhook: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@webhooks_bp.route('/consultation-reminder', methods=['POST'])
def consultation_reminder_webhook():
    """
    Webhook для напоминаний о консультациях
    """
    try:
        data = request.get_json()
        consultation_id = data.get('consultation_id')
        reminder_type = data.get('reminder_type', '24h')

        consultation = ConsultationRequest.query.get(consultation_id)
        if not consultation:
            return jsonify({'error': 'Consultation not found'}), 404

        # Отправка напоминания
        send_notification_email.delay(
            'consultation_reminder',
            consultation.email,
            {
                'consultation': consultation.to_dict(),
                'reminder_type': reminder_type
            }
        )

        return jsonify({
            'status': 'success',
            'message': 'Reminder sent'
        }), 200

    except Exception as e:
        current_app.logger.error(
            f'Error in consultation reminder webhook: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@webhooks_bp.route('/project-status', methods=['POST'])
def project_status_webhook():
    """
    Webhook для обновления статуса проектов
    """
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        new_status = data.get('status')

        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        old_status = project.status
        project.status = new_status
        project.updated_at = datetime.utcnow()
        db.session.commit()

        # Уведомление клиента об изменении статуса
        if project.client_email:
            send_notification_email.delay(
                'project_status_update',
                project.client_email,
                {
                    'project': project.to_dict(),
                    'old_status': old_status,
                    'new_status': new_status
                }
            )

        return jsonify({
            'status': 'success',
            'message': 'Project status updated',
            'project_id': project_id,
            'old_status': old_status,
            'new_status': new_status
        }), 200

    except Exception as e:
        current_app.logger.error(f'Error in project status webhook: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

# Обработчики событий n8n


def handle_lead_processed(payload):
    """Обработка события обработки лида"""
    lead_id = payload.get('lead_id')
    result = payload.get('result', {})

    if lead_id:
        lead = Lead.query.get(lead_id)
        if lead:
            lead.status = result.get('status', 'processed')
            lead.notes = result.get('notes', '')
            if result.get('assigned_to'):
                lead.assigned_to = result['assigned_to']
            db.session.commit()

    return {'lead_id': lead_id, 'status': 'updated'}


def handle_email_sent(payload):
    """Обработка события отправки email"""
    email_id = payload.get('email_id')
    status = payload.get('status')

    current_app.logger.info(f'Email {email_id} status: {status}')

    return {'email_id': email_id, 'status': status}


def handle_consultation_scheduled(payload):
    """Обработка события планирования консультации"""
    consultation_id = payload.get('consultation_id')
    scheduled_time = payload.get('scheduled_time')

    if consultation_id:
        consultation = ConsultationRequest.query.get(consultation_id)
        if consultation:
            consultation.status = 'scheduled'
            consultation.scheduled_time = datetime.fromisoformat(
                scheduled_time)
            db.session.commit()

    return {
        'consultation_id': consultation_id,
        'scheduled_time': scheduled_time}


def handle_project_updated(payload):
    """Обработка события обновления проекта"""
    project_id = payload.get('project_id')
    updates = payload.get('updates', {})

    if project_id:
        project = Project.query.get(project_id)
        if project:
            for key, value in updates.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            project.updated_at = datetime.utcnow()
            db.session.commit()

    return {'project_id': project_id, 'updates': updates}


def handle_automation_completed(payload):
    """Обработка события завершения автоматизации"""
    automation_id = payload.get('automation_id')
    result = payload.get('result')

    current_app.logger.info(
        f'Automation {automation_id} completed with result: {result}')

    return {'automation_id': automation_id, 'result': result}


@webhooks_bp.route('/health', methods=['GET'])
def webhook_health():
    """Health check для webhook endpoints"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': [
            '/webhooks/n8n',
            '/webhooks/lead-automation',
            '/webhooks/consultation-reminder',
            '/webhooks/project-status'
        ]
    }), 200
