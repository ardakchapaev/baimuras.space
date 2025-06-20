
"""Обновленные модели данных для мебельной платформы BaiMuras."""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from sqlalchemy import Numeric

db = SQLAlchemy()

class OrderStatus(Enum):
    """Статусы заказов."""
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PRODUCTION = "in_production"
    READY = "ready"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ProjectStatus(Enum):
    """Статусы проектов."""
    CONSULTATION = "consultation"
    MEASUREMENT = "measurement"
    DESIGN = "design"
    APPROVAL = "approval"
    PRODUCTION = "production"
    INSTALLATION = "installation"
    COMPLETED = "completed"

class LeadStatus(Enum):
    """Статусы лидов."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CONVERTED = "converted"
    LOST = "lost"

class FurnitureType(Enum):
    """Типы мебели."""
    KITCHEN = "kitchen"
    BEDROOM = "bedroom"
    LIVING_ROOM = "living_room"
    CHILDREN_ROOM = "children_room"
    OFFICE = "office"
    WARDROBE = "wardrobe"
    MONTESSORI = "montessori"
    CUSTOM = "custom"

# Связующая таблица многие-ко-многим для проектов и услуг
project_services = db.Table('project_services',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    """Модель пользователя."""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='client')  # admin, manager, client
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Связи
    leads = db.relationship('Lead', backref='client', lazy=True)
    projects = db.relationship('Project', backref='client', lazy=True)
    consultations = db.relationship('ConsultationRequest', backref='client', lazy=True)
    
    def set_password(self, password):
        """Установка хэша пароля."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверка пароля."""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Полное имя пользователя."""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'

class Lead(db.Model):
    """Модель лида."""
    __tablename__ = 'lead'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    furniture_type = db.Column(db.Enum(FurnitureType), nullable=False)
    budget_range = db.Column(db.String(50))
    description = db.Column(db.Text)
    status = db.Column(db.Enum(LeadStatus), default=LeadStatus.NEW)
    source = db.Column(db.String(50))  # website, referral, social_media, etc.
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Связи
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_leads')
    
    def __repr__(self):
        return f'<Lead {self.name} - {self.furniture_type.value}>'

class Service(db.Model):
    """Модель услуги."""
    __tablename__ = 'service'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    furniture_type = db.Column(db.Enum(FurnitureType), nullable=False)
    base_price = db.Column(Numeric(10, 2))
    unit = db.Column(db.String(20))  # кв.м, шт, комплект
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<Service {self.name}>'

class Project(db.Model):
    """Модель проекта."""
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))  # Если конвертирован из лида
    status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.CONSULTATION)
    furniture_type = db.Column(db.Enum(FurnitureType), nullable=False)
    
    # Финансовые данные
    estimated_budget = db.Column(Numeric(10, 2))
    final_cost = db.Column(Numeric(10, 2))
    
    # Даты
    start_date = db.Column(db.Date)
    expected_completion = db.Column(db.Date)
    actual_completion = db.Column(db.Date)
    measurement_date = db.Column(db.Date)
    
    # Адрес проекта
    address = db.Column(db.String(200))
    room_count = db.Column(db.Integer)
    total_area = db.Column(Numeric(5, 2))
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Связи
    lead = db.relationship('Lead', backref='converted_project')
    services = db.relationship('Service', secondary=project_services, backref='projects')
    orders = db.relationship('Order', backref='project', lazy=True)
    measurements = db.relationship('Measurement', backref='project', lazy=True)
    project_files = db.relationship('ProjectFile', backref='project', lazy=True)
    
    @property
    def progress_percentage(self):
        """Процент выполнения проекта."""
        status_progress = {
            ProjectStatus.CONSULTATION: 10,
            ProjectStatus.MEASUREMENT: 20,
            ProjectStatus.DESIGN: 40,
            ProjectStatus.APPROVAL: 50,
            ProjectStatus.PRODUCTION: 80,
            ProjectStatus.INSTALLATION: 95,
            ProjectStatus.COMPLETED: 100
        }
        return status_progress.get(self.status, 0)
    
    def __repr__(self):
        return f'<Project {self.name}>'

class Order(db.Model):
    """Модель заказа."""
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Статус и даты
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.DRAFT)
    order_date = db.Column(db.Date, default=datetime.utcnow)
    expected_delivery = db.Column(db.Date)
    actual_delivery = db.Column(db.Date)
    
    # Финансовые данные
    subtotal = db.Column(Numeric(10, 2), nullable=False, default=0)
    discount = db.Column(Numeric(10, 2), default=0)
    tax = db.Column(Numeric(10, 2), default=0)
    total_amount = db.Column(Numeric(10, 2), nullable=False, default=0)
    
    # Оплата
    paid_amount = db.Column(Numeric(10, 2), default=0)
    payment_terms = db.Column(db.String(100))
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Связи
    client = db.relationship('User', backref='orders')
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    @property
    def remaining_balance(self):
        """Остаток к доплате."""
        return self.total_amount - self.paid_amount
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    """Позиция заказа."""
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    
    quantity = db.Column(Numeric(8, 2), nullable=False, default=1)
    unit_price = db.Column(Numeric(10, 2), nullable=False)
    total_price = db.Column(Numeric(10, 2), nullable=False)
    
    description = db.Column(db.String(200))
    specifications = db.Column(db.Text)
    
    # Связи
    service = db.relationship('Service', backref='order_items')
    
    def __repr__(self):
        return f'<OrderItem {self.service.name} x {self.quantity}>'

class ConsultationRequest(db.Model):
    """Модель запроса на консультацию."""
    __tablename__ = 'consultation_request'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    furniture_type = db.Column(db.Enum(FurnitureType), nullable=False)
    consultation_type = db.Column(db.String(50))  # home_visit, office_visit, online
    preferred_date = db.Column(db.Date)
    preferred_time = db.Column(db.Time)
    
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, scheduled, completed, cancelled
    
    # Назначенная консультация
    scheduled_date = db.Column(db.DateTime)
    consultant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Связи
    consultant = db.relationship('User', foreign_keys=[consultant_id], backref='consultations_assigned')
    
    def __repr__(self):
        return f'<ConsultationRequest {self.name} - {self.furniture_type.value}>'

class Measurement(db.Model):
    """Модель замера."""
    __tablename__ = 'measurement'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    measurer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    scheduled_date = db.Column(db.DateTime, nullable=False)
    actual_date = db.Column(db.DateTime)
    duration_hours = db.Column(Numeric(3, 1))
    
    # Результаты замера
    measurements_data = db.Column(db.JSON)  # Сохранение размеров в JSON
    photos = db.Column(db.JSON)  # Пути к фотографиям
    notes = db.Column(db.Text)
    
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, rescheduled
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Связи
    measurer = db.relationship('User', backref='measurements_taken')
    
    def __repr__(self):
        return f'<Measurement {self.project.name} - {self.scheduled_date}>'

class ProjectFile(db.Model):
    """Файлы проекта."""
    __tablename__ = 'project_file'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(50))  # design, photo, document, specification
    mime_type = db.Column(db.String(100))
    
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Связи
    uploaded_by = db.relationship('User', backref='uploaded_files')
    
    def __repr__(self):
        return f'<ProjectFile {self.original_filename}>'

# Для совместимости с существующим кодом
Role = User
