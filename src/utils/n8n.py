"""
Интеграция с n8n для автоматизации бизнес-процессов
"""
import requests
import os
import json
import hmac
import hashlib
from datetime import datetime
from flask import current_app
from typing import Dict, Any, Optional, List

class N8NClient:
    """Клиент для работы с n8n API и webhook'ами"""
    
    def __init__(self):
        self.webhook_url = os.getenv('N8N_WEBHOOK_URL')
        self.api_url = os.getenv('N8N_API_URL', 'http://localhost:5678/api/v1')
        self.api_key = os.getenv('N8N_API_KEY')
        self.webhook_secret = os.getenv('N8N_WEBHOOK_SECRET')
        self.timeout = int(os.getenv('N8N_TIMEOUT', '30'))
        
    def _generate_signature(self, payload: str) -> str:
        """Генерация подписи для webhook"""
        if not self.webhook_secret:
            return ''
        
        return hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict]:
        """Базовый метод для HTTP запросов"""
        try:
            headers = kwargs.get('headers', {})
            if self.api_key:
                headers['X-N8N-API-KEY'] = self.api_key
            headers['Content-Type'] = 'application/json'
            kwargs['headers'] = headers
            
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            if current_app:
                current_app.logger.error(f'N8N request failed: {str(e)}')
            return None
        except Exception as e:
            if current_app:
                current_app.logger.error(f'Unexpected error in N8N request: {str(e)}')
            return None
    
    def send_webhook(self, data: Dict[str, Any], webhook_url: Optional[str] = None) -> bool:
        """
        Отправка данных в n8n webhook
        
        Args:
            data: Данные для отправки
            webhook_url: Альтернативный URL webhook'а
        
        Returns:
            bool: Успешность отправки
        """
        try:
            url = webhook_url or self.webhook_url
            if not url:
                if current_app:
                    current_app.logger.warning('N8N webhook URL not configured')
                return False
            
            # Добавление метаданных
            payload = {
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'baimuras-platform',
                'data': data
            }
            
            payload_str = json.dumps(payload, ensure_ascii=False)
            headers = {'Content-Type': 'application/json'}
            
            # Добавление подписи если настроена
            if self.webhook_secret:
                signature = self._generate_signature(payload_str)
                headers['X-N8N-Signature'] = f'sha256={signature}'
            
            response = requests.post(
                url, 
                data=payload_str, 
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            if current_app:
                current_app.logger.info(f'Successfully sent webhook to n8n: {data.get("event_type", "unknown")}')
            return True
            
        except requests.exceptions.RequestException as e:
            if current_app:
                current_app.logger.error(f'Failed to send webhook to n8n: {str(e)}')
            return False
        except Exception as e:
            if current_app:
                current_app.logger.error(f'Unexpected error sending webhook to n8n: {str(e)}')
            return False

# Глобальный экземпляр клиента
n8n_client = N8NClient()

# Обратная совместимость
N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')

def send_event(event: str, payload: dict) -> None:
    """Send event data to n8n if webhook url configured (обратная совместимость)."""
    if not N8N_WEBHOOK_URL:
        return
    try:
        data = {"event": event, "data": payload}
        n8n_client.send_webhook(data)
    except Exception:
        pass

def send_to_n8n(data: Dict[str, Any], webhook_url: Optional[str] = None) -> bool:
    """
    Отправка данных в n8n webhook
    
    Args:
        data: Данные для отправки
        webhook_url: Альтернативный URL webhook'а
    
    Returns:
        bool: Успешность отправки
    """
    return n8n_client.send_webhook(data, webhook_url)

def send_lead_to_automation(lead_data: Dict[str, Any]) -> bool:
    """
    Отправка данных лида в автоматизацию
    
    Args:
        lead_data: Данные лида
    
    Returns:
        bool: Успешность отправки
    """
    automation_data = {
        'event_type': 'new_lead',
        'lead': lead_data,
        'automation_type': 'lead_processing'
    }
    
    return n8n_client.send_webhook(automation_data)

def send_consultation_to_automation(consultation_data: Dict[str, Any]) -> bool:
    """
    Отправка данных консультации в автоматизацию
    
    Args:
        consultation_data: Данные консультации
    
    Returns:
        bool: Успешность отправки
    """
    automation_data = {
        'event_type': 'new_consultation',
        'consultation': consultation_data,
        'automation_type': 'consultation_scheduling'
    }
    
    return n8n_client.send_webhook(automation_data)

def send_project_update_to_automation(project_data: Dict[str, Any], update_type: str) -> bool:
    """
    Отправка обновления проекта в автоматизацию
    
    Args:
        project_data: Данные проекта
        update_type: Тип обновления (created, updated, completed, etc.)
    
    Returns:
        bool: Успешность отправки
    """
    automation_data = {
        'event_type': 'project_update',
        'project': project_data,
        'update_type': update_type,
        'automation_type': 'project_management'
    }
    
    return n8n_client.send_webhook(automation_data)

def send_email_automation_request(email_data: Dict[str, Any]) -> bool:
    """
    Запрос автоматической отправки email через n8n
    
    Args:
        email_data: Данные для email
    
    Returns:
        bool: Успешность отправки
    """
    automation_data = {
        'event_type': 'email_request',
        'email': email_data,
        'automation_type': 'email_sending'
    }
    
    return n8n_client.send_webhook(automation_data)

def trigger_backup_automation() -> bool:
    """
    Запуск автоматизации резервного копирования
    
    Returns:
        bool: Успешность запуска
    """
    automation_data = {
        'event_type': 'backup_request',
        'timestamp': datetime.utcnow().isoformat(),
        'automation_type': 'backup'
    }
    
    return n8n_client.send_webhook(automation_data)

def trigger_analytics_automation(analytics_type: str, parameters: Dict[str, Any] = None) -> bool:
    """
    Запуск автоматизации аналитики
    
    Args:
        analytics_type: Тип аналитики (daily, weekly, monthly)
        parameters: Дополнительные параметры
    
    Returns:
        bool: Успешность запуска
    """
    automation_data = {
        'event_type': 'analytics_request',
        'analytics_type': analytics_type,
        'parameters': parameters or {},
        'automation_type': 'analytics'
    }
    
    return n8n_client.send_webhook(automation_data)
