
"""Обновленные основные маршруты для мебельной платформы BaiMuras."""

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from datetime import datetime
import json

from src.models.updated_models import db, Lead, Project, ConsultationRequest, Service, FurnitureType, LeadStatus
from src.utils import get_current_language
from automation.tasks.email_tasks import send_consultation_confirmation, send_welcome_email

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Главная страница."""
    # Получаем последние проекты для портфолио
    recent_projects = Project.query.filter_by(status='completed').limit(6).all()
    
    # Статистика для главной страницы
    stats = {
        'completed_projects': Project.query.filter_by(status='completed').count(),
        'happy_clients': len(set([p.client_id for p in Project.query.all()])),
        'years_experience': 10
    }
    
    return render_template('index_updated.html', 
                         recent_projects=recent_projects,
                         stats=stats)

@main_bp.route('/about')
def about():
    """О компании."""
    team_members = [
        {
            'name': 'Арстан Чапаев',
            'position': 'Основатель и главный дизайнер',
            'experience': '15 лет',
            'specialization': 'Дизайн интерьера, проектирование',
            'image': 'team-arstan.jpg'
        },
        {
            'name': 'Гульмира Токтосунова',
            'position': 'Менеджер проектов',
            'experience': '8 лет',
            'specialization': 'Управление проектами, клиентский сервис',
            'image': 'team-gulmira.jpg'
        },
        {
            'name': 'Бекзат Иманалиев',
            'position': 'Мастер-краснодеревщик',
            'experience': '12 лет',
            'specialization': 'Изготовление корпусной мебели',
            'image': 'team-bekzat.jpg'
        }
    ]
    
    company_values = [
        {
            'title': 'Качество',
            'description': 'Используем только проверенные материалы и фурнитуру',
            'icon': 'fa-medal'
        },
        {
            'title': 'Индивидуальность',
            'description': 'Каждый проект уникален и создается под клиента',
            'icon': 'fa-user-cog'
        },
        {
            'title': 'Надежность',
            'description': 'Гарантируем долговечность нашей мебели',
            'icon': 'fa-shield-alt'
        },
        {
            'title': 'Экологичность',
            'description': 'Заботимся об окружающей среде и здоровье',
            'icon': 'fa-leaf'
        }
    ]
    
    return render_template('about.html',
                         team_members=team_members,
                         company_values=company_values)

@main_bp.route('/services')
def services():
    """Все услуги."""
    services_list = [
        {
            'name': 'Кухни на заказ',
            'description': 'Современные кухонные гарнитуры с индивидуальным дизайном',
            'features': ['3D-проектирование', 'Качественная фурнитура', 'Монтаж и подключение'],
            'price_from': 25000,
            'image': 'kitchen-service.jpg',
            'url': 'main.services_kitchens'
        },
        {
            'name': 'Шкафы и гардеробные',
            'description': 'Встроенные и корпусные шкафы, гардеробные системы',
            'features': ['Системы хранения', 'Раздвижные механизмы', 'Освещение LED'],
            'price_from': 18000,
            'image': 'wardrobe-service.jpg',
            'url': 'main.services_wardrobes'
        },
        {
            'name': 'Детская мебель',
            'description': 'Безопасная и функциональная мебель для детских комнат',
            'features': ['Безопасные материалы', 'Растущая мебель', 'Яркий дизайн'],
            'price_from': 15000,
            'image': 'children-service.jpg',
            'url': 'main.services_children_rooms'
        },
        {
            'name': 'Мебель Монтессори',
            'description': 'Развивающая мебель по методике Монтессори',
            'features': ['Методика Монтессори', 'Натуральные материалы', 'Адаптивная высота'],
            'price_from': 12000,
            'image': 'montessori-service.jpg',
            'url': 'main.services_montessori'
        },
        {
            'name': 'Офисная мебель',
            'description': 'Эргономичные решения для рабочих пространств',
            'features': ['Эргономичный дизайн', 'Организация пространства', 'Современный стиль'],
            'price_from': 20000,
            'image': 'office-service.jpg',
            'url': 'main.services_office'
        },
        {
            'name': 'Прихожие и коридоры',
            'description': 'Функциональные решения для входных зон',
            'features': ['Системы хранения', 'Зеркальные фасады', 'Освещение'],
            'price_from': 16000,
            'image': 'hallway-service.jpg',
            'url': 'main.services_hallway'
        }
    ]
    
    return render_template('services.html', services_list=services_list)

@main_bp.route('/services/kitchens')
def services_kitchens():
    """Кухни на заказ."""
    return render_template('services/kitchens.html')

@main_bp.route('/services/wardrobes')
def services_wardrobes():
    """Шкафы и гардеробные."""
    return render_template('services/wardrobes.html')

@main_bp.route('/services/children-rooms')
def services_children_rooms():
    """Детская мебель."""
    return render_template('services/children-rooms.html')

@main_bp.route('/services/montessori')
def services_montessori():
    """Мебель Монтессори."""
    return render_template('services/montessori.html')

@main_bp.route('/services/office')
def services_office():
    """Офисная мебель."""
    return render_template('services/office.html')

@main_bp.route('/services/hallway')
def services_hallway():
    """Прихожие и коридоры."""
    return render_template('services/hallway.html')

@main_bp.route('/portfolio')
def portfolio():
    """Портфолио проектов."""
    # Фильтрация по типу мебели
    furniture_type = request.args.get('type', 'all')
    
    query = Project.query.filter_by(status='completed')
    
    if furniture_type != 'all':
        try:
            enum_type = FurnitureType(furniture_type)
            query = query.filter_by(furniture_type=enum_type)
        except ValueError:
            pass
    
    projects = query.order_by(Project.actual_completion.desc()).all()
    
    # Категории для фильтра
    categories = [
        {'value': 'all', 'label': 'Все проекты'},
        {'value': 'kitchen', 'label': 'Кухни'},
        {'value': 'wardrobe', 'label': 'Шкафы'},
        {'value': 'children_room', 'label': 'Детская мебель'},
        {'value': 'montessori', 'label': 'Монтессори'},
        {'value': 'office', 'label': 'Офисная мебель'},
        {'value': 'living_room', 'label': 'Гостиная'}
    ]
    
    return render_template('portfolio.html',
                         projects=projects,
                         categories=categories,
                         selected_category=furniture_type)

@main_bp.route('/calculator')
def calculator():
    """Калькулятор стоимости."""
    furniture_types = [
        {'value': 'kitchen', 'label': 'Кухня', 'base_price': 25000},
        {'value': 'wardrobe', 'label': 'Шкаф', 'base_price': 18000},
        {'value': 'children_room', 'label': 'Детская мебель', 'base_price': 15000},
        {'value': 'montessori', 'label': 'Мебель Монтессори', 'base_price': 12000},
        {'value': 'office', 'label': 'Офисная мебель', 'base_price': 20000},
        {'value': 'living_room', 'label': 'Гостиная', 'base_price': 22000}
    ]
    
    materials = [
        {'value': 'laminate', 'label': 'ЛДСП', 'multiplier': 1.0},
        {'value': 'mdf', 'label': 'МДФ', 'multiplier': 1.3},
        {'value': 'natural_wood', 'label': 'Натуральное дерево', 'multiplier': 2.0},
        {'value': 'acrylic', 'label': 'Акрил', 'multiplier': 1.8}
    ]
    
    return render_template('calculator.html',
                         furniture_types=furniture_types,
                         materials=materials)

@main_bp.route('/calculate-price', methods=['POST'])
def calculate_price():
    """AJAX расчет стоимости."""
    try:
        data = request.get_json()
        
        # Базовые параметры
        furniture_type = data.get('furniture_type')
        material = data.get('material', 'laminate')
        area = float(data.get('area', 1))
        complexity = data.get('complexity', 'standard')
        
        # Базовые цены за м²
        base_prices = {
            'kitchen': 25000,
            'wardrobe': 18000,
            'children_room': 15000,
            'montessori': 12000,
            'office': 20000,
            'living_room': 22000
        }
        
        # Множители для материалов
        material_multipliers = {
            'laminate': 1.0,
            'mdf': 1.3,
            'natural_wood': 2.0,
            'acrylic': 1.8
        }
        
        # Множители для сложности
        complexity_multipliers = {
            'simple': 0.8,
            'standard': 1.0,
            'complex': 1.3,
            'premium': 1.6
        }
        
        base_price = base_prices.get(furniture_type, 20000)
        material_mult = material_multipliers.get(material, 1.0)
        complexity_mult = complexity_multipliers.get(complexity, 1.0)
        
        # Расчет стоимости
        total_price = base_price * area * material_mult * complexity_mult
        
        # Дополнительные услуги
        services = data.get('services', [])
        service_costs = {
            'design': total_price * 0.1,  # 10% от стоимости
            'delivery': 5000,
            'installation': total_price * 0.15,  # 15% от стоимости
            'warranty_extended': total_price * 0.05  # 5% от стоимости
        }
        
        additional_cost = sum(service_costs.get(service, 0) for service in services)
        final_price = total_price + additional_cost
        
        return jsonify({
            'success': True,
            'base_price': int(total_price),
            'additional_services': int(additional_cost),
            'total_price': int(final_price),
            'breakdown': {
                'base': int(base_price * area),
                'material_adjustment': int(base_price * area * (material_mult - 1)),
                'complexity_adjustment': int(base_price * area * material_mult * (complexity_mult - 1)),
                'services': {service: int(service_costs.get(service, 0)) for service in services}
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Контакты и форма обратной связи."""
    if request.method == 'POST':
        try:
            # Получение данных формы
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            furniture_type = request.form.get('furniture_type')
            message = request.form.get('message')
            consultation_type = request.form.get('consultation_type', 'phone')
            
            # Создание лида
            lead = Lead(
                name=name,
                email=email,
                phone=phone,
                furniture_type=FurnitureType(furniture_type),
                description=message,
                source='website',
                status=LeadStatus.NEW
            )
            
            # Создание запроса на консультацию
            consultation = ConsultationRequest(
                name=name,
                email=email,
                phone=phone,
                furniture_type=FurnitureType(furniture_type),
                consultation_type=consultation_type,
                message=message,
                status='pending'
            )
            
            db.session.add(lead)
            db.session.add(consultation)
            db.session.commit()
            
            # Отправка email подтверждения (асинхронно)
            send_consultation_confirmation.delay(consultation.id)
            
            flash('Спасибо за обращение! Мы свяжемся с вами в ближайшее время.', 'success')
            return redirect(url_for('main.contact'))
            
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при отправке заявки. Попробуйте еще раз.', 'error')
    
    # Контактная информация
    contact_info = {
        'phone': '+996 509 912 569',
        'email': 'info@baimuras.space',
        'address': 'г. Бишкек, ул. Фрунзе 123, Мебельный центр "Доника", 2 этаж',
        'working_hours': {
            'weekdays': 'Пн-Пт: 9:00-18:00',
            'saturday': 'Сб: 10:00-16:00',
            'sunday': 'Вс: выходной'
        },
        'coordinates': {
            'lat': 42.8746,
            'lng': 74.5698
        }
    }
    
    # Варианты мебели для формы
    furniture_options = [
        {'value': 'kitchen', 'label': 'Кухня'},
        {'value': 'wardrobe', 'label': 'Шкаф/Гардеробная'},
        {'value': 'children_room', 'label': 'Детская мебель'},
        {'value': 'montessori', 'label': 'Мебель Монтессори'},
        {'value': 'office', 'label': 'Офисная мебель'},
        {'value': 'living_room', 'label': 'Гостиная'},
        {'value': 'custom', 'label': 'Другое'}
    ]
    
    return render_template('contact.html',
                         contact_info=contact_info,
                         furniture_options=furniture_options)

@main_bp.route('/blog')
def blog():
    """Блог (заглушка)."""
    return render_template('blog.html')

@main_bp.route('/set-language/<language>')
def set_language_route(language):
    """Смена языка."""
    if language in ['ru', 'ky']:
        session['language'] = language
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/search')
def search():
    """Поиск по сайту."""
    query = request.args.get('q', '').strip()
    results = []
    
    if query:
        # Поиск в проектах
        projects = Project.query.filter(
            Project.name.contains(query) | 
            Project.description.contains(query)
        ).limit(10).all()
        
        for project in projects:
            results.append({
                'type': 'project',
                'title': project.name,
                'description': project.description[:200] + '...' if len(project.description) > 200 else project.description,
                'url': url_for('main.portfolio') + f'#{project.id}'
            })
    
    return render_template('search_results.html', 
                         query=query, 
                         results=results)

# API endpoints для фронтенда
@main_bp.route('/api/furniture-types')
def api_furniture_types():
    """API: Получение типов мебели."""
    types = [
        {'value': ft.value, 'label': ft.value.replace('_', ' ').title()}
        for ft in FurnitureType
    ]
    return jsonify(types)

@main_bp.route('/api/quick-quote', methods=['POST'])
def api_quick_quote():
    """API: Быстрая оценка стоимости."""
    try:
        data = request.get_json()
        furniture_type = data.get('type')
        area = float(data.get('area', 1))
        
        base_prices = {
            'kitchen': 25000,
            'wardrobe': 18000,
            'children_room': 15000,
            'montessori': 12000,
            'office': 20000,
            'living_room': 22000
        }
        
        estimated_price = base_prices.get(furniture_type, 20000) * area
        
        return jsonify({
            'success': True,
            'estimated_price': int(estimated_price),
            'currency': 'сом',
            'note': 'Предварительная оценка. Точная стоимость рассчитывается после замера.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Обработчики ошибок
@main_bp.errorhandler(404)
def not_found_error(error):
    """Обработчик 404 ошибки."""
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """Обработчик 500 ошибки."""
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Context processors
@main_bp.app_context_processor
def inject_furniture_data():
    """Внедрение данных о мебели в контекст."""
    return {
        'furniture_types': [
            {'value': ft.value, 'label': ft.value.replace('_', ' ').title()}
            for ft in FurnitureType
        ],
        'current_year': datetime.now().year
    }
