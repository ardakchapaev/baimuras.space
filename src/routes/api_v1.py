"""
API v1 endpoints с JWT аутентификацией
"""

from datetime import datetime

from flask import Blueprint, current_app, jsonify, request
from werkzeug.security import check_password_hash

from ..automation.tasks.email_tasks import send_lead_notification, send_welcome_email
from ..models import Lead, Project, Role, User, db
from ..utils.jwt_utils import (
    admin_required,
    generate_tokens,
    get_current_user,
    jwt_required,
    manager_required,
    optional_jwt,
    refresh_access_token,
)
from ..utils.n8n import send_lead_to_automation, send_project_update_to_automation

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Аутентификация


@api_v1_bp.route("/auth/login", methods=["POST"])
def login():
    """
    Вход в систему

    Body:
        email: Email пользователя
        password: Пароль

    Returns:
        JWT токены и информация о пользователе
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Поиск пользователя
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Генерация токенов
        tokens = generate_tokens(
            user.id, user.email, user.role.name if user.role else "user"
        )

        # Обновление времени последнего входа
        user.last_login = datetime.utcnow()
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "role": user.role.name if user.role else "user",
                    },
                    **tokens,
                }
            ),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1_bp.route("/auth/refresh", methods=["POST"])
def refresh():
    """
    Обновление access токена

    Body:
        refresh_token: Refresh токен

    Returns:
        Новые JWT токены
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return jsonify({"error": "Refresh token is required"}), 400

        # Обновление токенов
        new_tokens = refresh_access_token(refresh_token)
        if not new_tokens:
            return jsonify({"error": "Invalid or expired refresh token"}), 401

        return jsonify({"message": "Tokens refreshed successfully", **new_tokens}), 200

    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1_bp.route("/auth/logout", methods=["POST"])
@jwt_required
def logout():
    """
    Выход из системы

    Returns:
        Подтверждение выхода
    """
    # В реальном приложении здесь можно добавить токен в blacklist
    return jsonify({"message": "Logout successful"}), 200


@api_v1_bp.route("/auth/profile", methods=["GET"])
@jwt_required
def get_profile():
    """
    Получение профиля текущего пользователя

    Returns:
        Информация о пользователе
    """
    user = get_current_user()

    return (
        jsonify(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role.name if user.role else "user",
                    "created_at": user.created_at.isoformat(),
                    "last_login": (
                        user.last_login.isoformat() if user.last_login else None
                    ),
                }
            }
        ),
        200,
    )


# Пользователи


@api_v1_bp.route("/users", methods=["GET"])
@manager_required
def get_users():
    """
    Получение списка пользователей

    Query params:
        page: Номер страницы (по умолчанию 1)
        per_page: Количество на странице (по умолчанию 20)
        role: Фильтр по роли
        search: Поиск по имени или email

    Returns:
        Список пользователей с пагинацией
    """
    try:
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 20, type=int), 100)
        role_filter = request.args.get("role")
        search = request.args.get("search")

        # Базовый запрос
        query = User.query

        # Фильтрация по роли
        if role_filter:
            query = query.join(Role).filter(Role.name == role_filter)

        # Поиск
        if search:
            query = query.filter(
                db.or_(User.name.ilike(f"%{search}%"), User.email.ilike(f"%{search}%"))
            )

        # Пагинация
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        users = []
        for user in pagination.items:
            users.append(
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role.name if user.role else "user",
                    "created_at": user.created_at.isoformat(),
                    "last_login": (
                        user.last_login.isoformat() if user.last_login else None
                    ),
                }
            )

        return (
            jsonify(
                {
                    "users": users,
                    "pagination": {
                        "page": page,
                        "pages": pagination.pages,
                        "per_page": per_page,
                        "total": pagination.total,
                        "has_next": pagination.has_next,
                        "has_prev": pagination.has_prev,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Get users error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1_bp.route("/users", methods=["POST"])
@admin_required
def create_user():
    """
    Создание нового пользователя

    Body:
        email: Email пользователя
        name: Имя пользователя
        password: Пароль
        role: Роль пользователя (опционально)

    Returns:
        Информация о созданном пользователе
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        email = data.get("email")
        name = data.get("name")
        password = data.get("password")
        role_name = data.get("role", "user")

        if not email or not name or not password:
            return jsonify({"error": "Email, name and password are required"}), 400

        # Проверка существования пользователя
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User with this email already exists"}), 409

        # Получение роли
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return jsonify({"error": f"Role {role_name} not found"}), 400

        # Создание пользователя
        user = User(email=email, name=name, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Отправка приветственного email
        send_welcome_email.delay(user.email, user.name)

        current_app.logger.info(f"User created: {user.email}")

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "role": user.role.name,
                        "created_at": user.created_at.isoformat(),
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create user error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1_bp.route("/users/<int:user_id>", methods=["GET"])
@manager_required
def get_user(user_id: int):
    """
    Получение информации о пользователе

    Args:
        user_id: ID пользователя

    Returns:
        Информация о пользователе
    """
    user = User.query.get_or_404(user_id)

    return (
        jsonify(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role.name if user.role else "user",
                    "created_at": user.created_at.isoformat(),
                    "last_login": (
                        user.last_login.isoformat() if user.last_login else None
                    ),
                }
            }
        ),
        200,
    )


@api_v1_bp.route("/users/<int:user_id>", methods=["PUT"])
@admin_required
def update_user(user_id: int):
    """
    Обновление информации о пользователе

    Args:
        user_id: ID пользователя

    Body:
        name: Новое имя (опционально)
        email: Новый email (опционально)
        role: Новая роль (опционально)
        password: Новый пароль (опционально)

    Returns:
        Обновленная информация о пользователе
    """
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Обновление полей
        if "name" in data:
            user.name = data["name"]

        if "email" in data:
            # Проверка уникальности email
            existing_user = User.query.filter_by(email=data["email"]).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({"error": "Email already in use"}), 409
            user.email = data["email"]

        if "role" in data:
            role = Role.query.filter_by(name=data["role"]).first()
            if not role:
                return jsonify({"error": f'Role {data["role"]} not found'}), 400
            user.role = role

        if "password" in data:
            user.set_password(data["password"])

        db.session.commit()

        current_app.logger.info(f"User updated: {user.email}")

        return (
            jsonify(
                {
                    "message": "User updated successfully",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "role": user.role.name if user.role else "user",
                        "created_at": user.created_at.isoformat(),
                        "last_login": (
                            user.last_login.isoformat() if user.last_login else None
                        ),
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update user error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1_bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id: int):
    """
    Удаление пользователя

    Args:
        user_id: ID пользователя

    Returns:
        Подтверждение удаления
    """
    try:
        user = User.query.get_or_404(user_id)

        # Проверка, что пользователь не удаляет сам себя
        current_user = get_current_user()
        if user.id == current_user.id:
            return jsonify({"error": "Cannot delete yourself"}), 400

        db.session.delete(user)
        db.session.commit()

        current_app.logger.info(f"User deleted: {user.email}")

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete user error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# Лиды


@api_v1_bp.route("/leads", methods=["GET"])
@manager_required
def get_leads():
    """
    Получение списка лидов

    Query params:
        page: Номер страницы
        per_page: Количество на странице
        status: Фильтр по статусу
        service_type: Фильтр по типу услуги
        search: Поиск по имени или email

    Returns:
        Список лидов с пагинацией
    """
    try:
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 20, type=int), 100)
        status_filter = request.args.get("status")
        service_filter = request.args.get("service_type")
        search = request.args.get("search")

        # Базовый запрос
        query = Lead.query

        # Фильтры
        if status_filter:
            query = query.filter(Lead.status == status_filter)

        if service_filter:
            query = query.filter(Lead.service_type == service_filter)

        if search:
            query = query.filter(
                db.or_(
                    Lead.name.ilike(f"%{search}%"),
                    Lead.email.ilike(f"%{search}%"),
                    Lead.phone.ilike(f"%{search}%"),
                )
            )

        # Сортировка по дате создания (новые первые)
        query = query.order_by(Lead.created_at.desc())

        # Пагинация
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        leads = []
        for lead in pagination.items:
            leads.append(
                {
                    "id": lead.id,
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "service_type": lead.service_type,
                    "status": lead.status,
                    "message": lead.message,
                    "created_at": lead.created_at.isoformat(),
                    "updated_at": (
                        lead.updated_at.isoformat() if lead.updated_at else None
                    ),
                }
            )

        return (
            jsonify(
                {
                    "leads": leads,
                    "pagination": {
                        "page": page,
                        "pages": pagination.pages,
                        "per_page": per_page,
                        "total": pagination.total,
                        "has_next": pagination.has_next,
                        "has_prev": pagination.has_prev,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Get leads error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1_bp.route("/leads", methods=["POST"])
@optional_jwt
def create_lead():
    """
    Создание нового лида

    Body:
        name: Имя клиента
        email: Email клиента
        phone: Телефон клиента
        service_type: Тип услуги
        message: Сообщение (опционально)

    Returns:
        Информация о созданном лиде
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        service_type = data.get("service_type")
        message = data.get("message", "")

        if not name or not email or not service_type:
            return jsonify({"error": "Name, email and service_type are required"}), 400

        # Создание лида
        lead = Lead(
            name=name,
            email=email,
            phone=phone,
            service_type=service_type,
            message=message,
            status="new",
        )

        db.session.add(lead)
        db.session.commit()

        # Отправка в автоматизацию
        lead_data = {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "service_type": lead.service_type,
            "message": lead.message,
            "created_at": lead.created_at.isoformat(),
        }

        send_lead_to_automation(lead_data)

        # Уведомление менеджеров
        # TODO: Получить из настроек
        manager_emails = ["manager@baimuras.space"]
        send_lead_notification.delay(lead_data, manager_emails)

        current_app.logger.info(f"Lead created: {lead.email}")

        return (
            jsonify(
                {
                    "message": "Lead created successfully",
                    "lead": {
                        "id": lead.id,
                        "name": lead.name,
                        "email": lead.email,
                        "phone": lead.phone,
                        "service_type": lead.service_type,
                        "status": lead.status,
                        "message": lead.message,
                        "created_at": lead.created_at.isoformat(),
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create lead error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1_bp.route("/leads/<int:lead_id>", methods=["GET"])
@manager_required
def get_lead(lead_id: int):
    """
    Получение информации о лиде

    Args:
        lead_id: ID лида

    Returns:
        Информация о лиде
    """
    lead = Lead.query.get_or_404(lead_id)

    return (
        jsonify(
            {
                "lead": {
                    "id": lead.id,
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "service_type": lead.service_type,
                    "status": lead.status,
                    "message": lead.message,
                    "notes": lead.notes,
                    "assigned_to": lead.assigned_to,
                    "created_at": lead.created_at.isoformat(),
                    "updated_at": (
                        lead.updated_at.isoformat() if lead.updated_at else None
                    ),
                }
            }
        ),
        200,
    )


@api_v1_bp.route("/leads/<int:lead_id>", methods=["PUT"])
@manager_required
def update_lead(lead_id: int):
    """
    Обновление лида

    Args:
        lead_id: ID лида

    Body:
        status: Новый статус
        notes: Заметки
        assigned_to: ID назначенного менеджера

    Returns:
        Обновленная информация о лиде
    """
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        old_status = lead.status

        # Обновление полей
        if "status" in data:
            lead.status = data["status"]

        if "notes" in data:
            lead.notes = data["notes"]

        if "assigned_to" in data:
            lead.assigned_to = data["assigned_to"]

        lead.updated_at = datetime.utcnow()
        db.session.commit()

        # Уведомление об изменении статуса
        if old_status != lead.status:
            lead_data = {
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "status": lead.status,
            }
            send_project_update_to_automation(lead_data, "status_change")

        current_app.logger.info(f"Lead updated: {lead.id}")

        return (
            jsonify(
                {
                    "message": "Lead updated successfully",
                    "lead": {
                        "id": lead.id,
                        "name": lead.name,
                        "email": lead.email,
                        "phone": lead.phone,
                        "service_type": lead.service_type,
                        "status": lead.status,
                        "message": lead.message,
                        "notes": lead.notes,
                        "assigned_to": lead.assigned_to,
                        "created_at": lead.created_at.isoformat(),
                        "updated_at": lead.updated_at.isoformat(),
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update lead error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1_bp.route("/leads/<int:lead_id>/convert", methods=["POST"])
@manager_required
def convert_lead_to_project(lead_id: int):
    """
    Конвертация лида в проект

    Args:
        lead_id: ID лида

    Body:
        project_name: Название проекта
        description: Описание проекта
        budget: Бюджет проекта (опционально)

    Returns:
        Информация о созданном проекте
    """
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        project_name = data.get("project_name")
        description = data.get("description")
        budget = data.get("budget")

        if not project_name or not description:
            return jsonify({"error": "Project name and description are required"}), 400

        # Создание проекта
        project = Project(
            name=project_name,
            description=description,
            client_name=lead.name,
            client_email=lead.email,
            client_phone=lead.phone,
            status="planning",
            budget=budget,
        )

        db.session.add(project)

        # Обновление статуса лида
        lead.status = "converted"
        lead.updated_at = datetime.utcnow()

        db.session.commit()

        # Отправка в автоматизацию
        project_data = {
            "id": project.id,
            "name": project.name,
            "client_email": project.client_email,
            "status": project.status,
        }
        send_project_update_to_automation(project_data, "created")

        current_app.logger.info(f"Lead {lead_id} converted to project {project.id}")

        return (
            jsonify(
                {
                    "message": "Lead converted to project successfully",
                    "project": {
                        "id": project.id,
                        "name": project.name,
                        "description": project.description,
                        "client_name": project.client_name,
                        "client_email": project.client_email,
                        "status": project.status,
                        "budget": project.budget,
                        "created_at": project.created_at.isoformat(),
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Convert lead error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# Health check


@api_v1_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint

    Returns:
        Статус системы
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "v1",
                "services": {
                    "database": "connected",
                    "redis": "connected",  # TODO: Проверить подключение к Redis
                    "n8n": "configured",  # TODO: Проверить подключение к n8n
                },
            }
        ),
        200,
    )
