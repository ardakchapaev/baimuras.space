from src.utils.logging_config import logger

#!/usr/bin/env python3
"""
Запуск модернизированного Flask приложения BaiMuras.
"""

from src.main_updated import app
import os
import sys
from flask.cli import FlaskGroup

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


cli = FlaskGroup(app)


@cli.command()
def create_db():
    """Создание базы данных."""
    from src.models.updated_models import db
    with app.app_context():
        db.create_all()
    logger.info("Database created successfully!")


@cli.command()
def init_db():
    """Инициализация базы данных с начальными данными."""
    from src.models.updated_models import (
        db, User, Service, FurnitureType
    )

    with app.app_context():
        db.create_all()

        # Создание администратора
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@baimuras.space',
                first_name='Администратор',
                last_name='BaiMuras',
                role='admin',
                phone='+996509912569'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)

        # Создание базовых услуг
        services_data = [{'name': 'Кухни на заказ',
                          'description': 'Современные кухонные гарнитуры с индивидуальным дизайном',
                          'furniture_type': FurnitureType.KITCHEN,
                          'base_price': 25000,
                          'unit': 'м²'},
                         {'name': 'Шкафы и гардеробные',
                          'description': 'Встроенные и корпусные шкафы, гардеробные системы',
                          'furniture_type': FurnitureType.WARDROBE,
                          'base_price': 18000,
                          'unit': 'м²'},
                         {'name': 'Детская мебель',
                          'description': 'Безопасная и функциональная мебель для детских комнат',
                          'furniture_type': FurnitureType.CHILDREN_ROOM,
                          'base_price': 15000,
                          'unit': 'м²'},
                         {'name': 'Мебель Монтессори',
                          'description': 'Развивающая мебель по методике Монтессори',
                          'furniture_type': FurnitureType.MONTESSORI,
                          'base_price': 12000,
                          'unit': 'шт'},
                         {'name': 'Офисная мебель',
                          'description': 'Эргономичные решения для рабочих пространств',
                          'furniture_type': FurnitureType.OFFICE,
                          'base_price': 20000,
                          'unit': 'м²'}]

        for service_data in services_data:
            existing_service = Service.query.filter_by(
                name=service_data['name']).first()
            if not existing_service:
                service = Service(**service_data)
                db.session.add(service)

        try:
            db.session.commit()
            logger.info("Database initialized successfully!")
            logger.info("Admin user created: admin / admin123")
        except Exception as e:
            db.session.rollback()
            logger.info(f"Error initializing database: {e}")


@cli.command()
def routes():
    """Показать все маршруты приложения."""
    import urllib.parse
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = urllib.parse.unquote(rule.build(options))
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        output.append(line)

    for line in sorted(output):
        logger.info(line)


if __name__ == '__main__':
    cli()
