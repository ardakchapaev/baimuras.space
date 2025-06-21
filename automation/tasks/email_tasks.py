"""Задачи для отправки email уведомлений."""

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from automation.celery_app import celery_app


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 60},
)
def send_welcome_email(self, user_email: str, user_name: str):
    """Отправка приветственного email новому пользователю."""
    try:
        subject = "Добро пожаловать в BaiMuras!"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: #6b70ba; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                    <h1 style="margin: 0;">BaiMuras</h1>
                    <p style="margin: 5px 0 0 0;">Мебельный инжиниринг</p>
                </div>

                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px;">
                    <h2 style="color: #6b70ba;">Добро пожаловать, {user_name}!</h2>

                    <p>Спасибо за регистрацию на платформе BaiMuras. Мы рады приветствовать вас в нашем сообществе любителей качественной мебели.</p>

                    <div style="background: white; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #6b70ba;">
                        <h3 style="margin-top: 0; color: #6b70ba;">Что вы можете делать:</h3>
                        <ul>
                            <li>Заказать консультацию по дизайну</li>
                            <li>Рассчитать стоимость проекта</li>
                            <li>Следить за прогрессом ваших заказов</li>
                            <li>Получать эксклюзивные предложения</li>
                        </ul>
                    </div>

                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://baimuras.space/services"
                           style="background: #6b70ba; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Изучить наши услуги
                        </a>
                    </div>

                    <p style="color: #666; font-size: 14px;">
                        Если у вас есть вопросы, свяжитесь с нами:<br>
                        📞 +996 509 912 569<br>
                        📧 info@baimuras.space
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return send_email(user_email, subject, html_content)

    except Exception as exc:
        self.retry(exc=exc)


@celery_app.task(bind=True)
def send_consultation_confirmation(self, consultation_id: int):
    """Отправка подтверждения консультации."""
    try:
        # Здесь можно получить данные консультации из БД
        subject = "Консультация BaiMuras - Подтверждение"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #6b70ba;">Консультация подтверждена</h2>
                <p>Ваша консультация по мебельному дизайну запланирована.</p>
                <p>Наш специалист свяжется с вами для уточнения деталей.</p>
            </div>
        </body>
        </html>
        """

        # В реальном приложении здесь будет получение email из БД
        return send_email("client@example.com", subject, html_content)

    except Exception as exc:
        self.retry(exc=exc)


@celery_app.task(bind=True)
def send_project_status_update(self, project_id: int, new_status: str):
    """Уведомление об изменении статуса проекта."""
    try:
        subject = f"Обновление статуса проекта - {new_status}"

        status_messages = {
            "measurement": "Запланирован замер помещения",
            "design": "Начата работа над дизайн-проектом",
            "approval": "Дизайн-проект готов к утверждению",
            "production": "Проект запущен в производство",
            "installation": "Мебель готова к установке",
            "completed": "Проект успешно завершен",
        }

        message = status_messages.get(new_status, "Статус проекта обновлен")

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #6b70ba;">Обновление по вашему проекту</h2>
                <p><strong>{message}</strong></p>
                <p>Войдите в личный кабинет для получения подробной информации.</p>
            </div>
        </body>
        </html>
        """

        return send_email("client@example.com", subject, html_content)

    except Exception as exc:
        self.retry(exc=exc)


@celery_app.task
def send_measurement_reminder(measurement_id: int):
    """Напоминание о предстоящем замере."""
    subject = "Напоминание о замере - BaiMuras"

    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #6b70ba;">Напоминание о замере</h2>
            <p>Завтра запланирован замер вашего помещения.</p>
            <p>Пожалуйста, подготовьте помещение и обеспечьте доступ нашему специалисту.</p>
        </div>
    </body>
    </html>
    """

    return send_email("client@example.com", subject, html_content)


def send_email(to_email: str, subject: str, html_content: str, attachments=None):
    """Универсальная функция отправки email."""
    try:
        # Настройки SMTP (в реальном приложении из конфигурации)
        smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        smtp_username = os.environ.get("SMTP_USERNAME", "")
        smtp_password = os.environ.get("SMTP_PASSWORD", "")
        from_email = os.environ.get("FROM_EMAIL", "info@baimuras.space")

        # Создание сообщения
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        # Добавление HTML контента
        html_part = MIMEText(html_content, "html", "utf-8")
        msg.attach(html_part)

        # Добавление вложений если есть
        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(attachment)}",
                    )
                    msg.attach(part)

        # Отправка email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return {"status": "success", "message": f"Email sent to {to_email}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
