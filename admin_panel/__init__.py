
"""Инициализация админ-панели BaiMuras."""

from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.exceptions import abort

class SecureModelView(ModelView):
    """Защищенная модель представления для админки."""
    
    def is_accessible(self):
        """Проверка доступа к админке."""
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        """Callback при отсутствии доступа."""
        abort(403)

class SecureAdminIndexView(AdminIndexView):
    """Защищенная главная страница админки."""
    
    def is_accessible(self):
        """Проверка доступа к админке."""
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        """Callback при отсутствии доступа."""
        abort(403)

def setup_admin_panel(app: Flask, db):
    """Настройка админ-панели."""
    
    admin = Admin(
        app,
        name='BaiMuras Admin',
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView()
    )
    
    # Импорт моделей
    from src.models.updated_models import (
        User, Lead, Project, Order, OrderItem, 
        ConsultationRequest, Service, Measurement, ProjectFile
    )
    
    # Добавление представлений моделей
    admin.add_view(SecureModelView(User, db.session, name='Пользователи'))
    admin.add_view(SecureModelView(Lead, db.session, name='Лиды'))
    admin.add_view(SecureModelView(Project, db.session, name='Проекты'))
    admin.add_view(SecureModelView(Order, db.session, name='Заказы'))
    admin.add_view(SecureModelView(OrderItem, db.session, name='Позиции заказов'))
    admin.add_view(SecureModelView(ConsultationRequest, db.session, name='Консультации'))
    admin.add_view(SecureModelView(Service, db.session, name='Услуги'))
    admin.add_view(SecureModelView(Measurement, db.session, name='Замеры'))
    admin.add_view(SecureModelView(ProjectFile, db.session, name='Файлы проектов'))
    
    return admin
