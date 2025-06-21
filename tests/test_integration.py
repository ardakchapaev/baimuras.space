"""
Интеграционные тесты для проверки автоматизации и API
"""
import pytest
import json
from unittest.mock import patch, MagicMock

from src.main import create_app
from src.models import db, User, Lead, Role
from src.utils.n8n import send_to_n8n, send_lead_to_automation
from src.utils.jwt_utils import generate_tokens


@pytest.fixture
def app():
    """Создание тестового приложения"""
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        # Создание тестовых ролей
        admin_role = Role(name='admin', description='Administrator')
        user_role = Role(name='user', description='User')
        db.session.add(admin_role)
        db.session.add(user_role)

        # Создание тестового пользователя
        test_user = User(
            email='test@baimuras.space',
            name='Test User',
            role=admin_role
        )
        test_user.set_password('testpass')
        db.session.add(test_user)

        db.session.commit()

        yield app

        db.drop_all()


@pytest.fixture
def client(app):
    """Тестовый клиент"""
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    """Заголовки с JWT токеном"""
    with app.app_context():
        user = User.query.filter_by(email='test@baimuras.space').first()
        tokens = generate_tokens(user.id, user.email, 'admin')
        return {'Authorization': f'Bearer {tokens["access_token"]}'}


class TestWebhookIntegration:
    """Тесты webhook интеграции"""

    def test_n8n_webhook_endpoint(self, client):
        """Тест n8n webhook endpoint"""
        webhook_data = {
            'event_type': 'test_event',
            'payload': {
                'test_data': 'test_value'
            }
        }

        response = client.post(
            '/api/webhooks/n8n',
            data=json.dumps(webhook_data),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'

    def test_lead_automation_webhook(self, client, app):
        """Тест webhook автоматизации лидов"""
        with app.app_context():
            # Создание тестового лида
            lead = Lead(
                name='Test Lead',
                email='lead@test.com',
                phone='+996555123456',
                service_type='design',
                message='Test message',
                status='new'
            )
            db.session.add(lead)
            db.session.commit()

            webhook_data = {
                'lead_id': lead.id
            }

            with patch('src.utils.n8n.send_to_n8n') as mock_n8n:
                mock_n8n.return_value = True

                response = client.post(
                    '/api/webhooks/lead-automation',
                    data=json.dumps(webhook_data),
                    content_type='application/json'
                )

                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['status'] == 'success'
                assert data['lead_id'] == lead.id

                # Проверка, что n8n был вызван
                mock_n8n.assert_called_once()


class TestAPIv1Integration:
    """Тесты API v1"""

    def test_auth_login(self, client, app):
        """Тест аутентификации"""
        login_data = {
            'email': 'test@baimuras.space',
            'password': 'testpass'
        }

        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == 'test@baimuras.space'

    def test_create_lead_via_api(self, client):
        """Тест создания лида через API"""
        lead_data = {
            'name': 'API Test Lead',
            'email': 'api@test.com',
            'phone': '+996555987654',
            'service_type': 'consultation',
            'message': 'API test message'
        }

        with patch('src.utils.n8n.send_lead_to_automation') as mock_automation:
            mock_automation.return_value = True

            response = client.post(
                '/api/v1/leads',
                data=json.dumps(lead_data),
                content_type='application/json'
            )

            assert response.status_code == 201
            data = json.loads(response.data)
            assert data['message'] == 'Lead created successfully'
            assert data['lead']['name'] == 'API Test Lead'

            # Проверка, что автоматизация была запущена
            mock_automation.assert_called_once()

    def test_get_leads_with_auth(self, client, auth_headers):
        """Тест получения лидов с аутентификацией"""
        response = client.get(
            '/api/v1/leads',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'leads' in data
        assert 'pagination' in data

    def test_convert_lead_to_project(self, client, auth_headers, app):
        """Тест конвертации лида в проект"""
        with app.app_context():
            # Создание тестового лида
            lead = Lead(
                name='Convert Test Lead',
                email='convert@test.com',
                phone='+996555111222',
                service_type='design',
                status='new'
            )
            db.session.add(lead)
            db.session.commit()

            conversion_data = {
                'project_name': 'Test Project',
                'description': 'Test project description',
                'budget': 50000
            }

            with patch('src.utils.n8n.send_project_update_to_automation') as mock_automation:
                mock_automation.return_value = True

                response = client.post(
                    f'/api/v1/leads/{lead.id}/convert',
                    data=json.dumps(conversion_data),
                    content_type='application/json',
                    headers=auth_headers
                )

                assert response.status_code == 201
                data = json.loads(response.data)
                assert data['message'] == 'Lead converted to project successfully'
                assert data['project']['name'] == 'Test Project'

                # Проверка, что автоматизация была запущена
                mock_automation.assert_called_once()


class TestN8NIntegration:
    """Тесты интеграции с n8n"""

    @patch('src.utils.n8n.requests.post')
    def test_send_to_n8n_success(self, mock_post):
        """Тест успешной отправки в n8n"""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        test_data = {
            'event_type': 'test',
            'data': {'test': 'value'}
        }

        result = send_to_n8n(test_data)
        assert result is True
        mock_post.assert_called_once()

    @patch('src.utils.n8n.requests.post')
    def test_send_to_n8n_failure(self, mock_post):
        """Тест неудачной отправки в n8n"""
        mock_post.side_effect = Exception('Connection error')

        test_data = {
            'event_type': 'test',
            'data': {'test': 'value'}
        }

        result = send_to_n8n(test_data)
        assert result is False

    def test_send_lead_to_automation(self):
        """Тест отправки лида в автоматизацию"""
        lead_data = {
            'id': 1,
            'name': 'Test Lead',
            'email': 'test@example.com',
            'service_type': 'design'
        }

        with patch('src.utils.n8n.n8n_client.send_webhook') as mock_webhook:
            mock_webhook.return_value = True

            result = send_lead_to_automation(lead_data)
            assert result is True
            mock_webhook.assert_called_once()

            # Проверка структуры данных
            call_args = mock_webhook.call_args[0][0]
            assert call_args['event_type'] == 'new_lead'
            assert call_args['lead'] == lead_data
            assert call_args['automation_type'] == 'lead_processing'


class TestCeleryIntegration:
    """Тесты интеграции с Celery"""

    @patch('automation.tasks.email_tasks.send_email')
    def test_send_welcome_email_task(self, mock_send_email):
        """Тест задачи отправки приветственного email"""
        from automation.tasks.email_tasks import send_welcome_email

        mock_send_email.return_value = {'status': 'success'}

        # Вызов задачи напрямую (без Celery)
        send_welcome_email('test@example.com', 'Test User')

        # Проверка, что email функция была вызвана
        mock_send_email.assert_called_once()

    @patch('automation.tasks.notification_tasks.send_lead_notification')
    def test_process_new_lead_event(self, mock_notification):
        """Тест обработки события нового лида"""
        from automation.tasks.notification_tasks import process_new_lead_event

        mock_notification.return_value = None

        payload = {
            'lead': {
                'id': 1,
                'name': 'Test Lead',
                'email': 'test@example.com'
            }
        }

        with patch('automation.tasks.notification_tasks.assign_lead_to_manager') as mock_assign, \
                patch('automation.tasks.notification_tasks.schedule_lead_followup') as mock_followup:

            mock_assign.return_value = None
            mock_followup.return_value = None

            result = process_new_lead_event(payload)

            assert result['status'] == 'success'
            assert result['lead_id'] == 1


class TestHealthChecks:
    """Тесты health check endpoints"""

    def test_api_health_check(self, client):
        """Тест health check API"""
        response = client.get('/api/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

    def test_api_v1_health_check(self, client):
        """Тест health check API v1"""
        response = client.get('/api/v1/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'services' in data

    def test_webhook_health_check(self, client):
        """Тест health check webhook"""
        response = client.get('/api/webhooks/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'endpoints' in data


class TestErrorHandling:
    """Тесты обработки ошибок"""

    def test_invalid_json_webhook(self, client):
        """Тест webhook с невалидным JSON"""
        response = client.post(
            '/api/webhooks/n8n',
            data='invalid json',
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_missing_auth_token(self, client):
        """Тест запроса без токена аутентификации"""
        response = client.get('/api/v1/leads')

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

    def test_invalid_auth_token(self, client):
        """Тест запроса с невалидным токеном"""
        headers = {'Authorization': 'Bearer invalid_token'}

        response = client.get('/api/v1/leads', headers=headers)

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
