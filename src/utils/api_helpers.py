"""
Вспомогательные функции для API endpoints
"""
from functools import wraps
from flask import jsonify, request
from src.utils.logging_config import logger


def validate_json_data(required_fields=None):
    """
    Декоратор для валидации JSON данных

    Args:
        required_fields (list): Список обязательных полей
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400

                if required_fields:
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        return jsonify({
                            'error': f'Missing required fields: {", ".join(missing_fields)}'
                        }), 400

                return f(data, *args, **kwargs)
            except Exception as e:
                logger.error(f"JSON validation error: {str(e)}")
                return jsonify({'error': 'Invalid JSON data'}), 400
        return decorated_function
    return decorator


def handle_api_errors(f):
    """
    Декоратор для централизованной обработки ошибок API
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {f.__name__}: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except PermissionError as e:
            logger.warning(f"Permission error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Access denied'}), 403
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function


def paginate_query(query, page=None, per_page=None):
    """
    Утилита для пагинации запросов

    Args:
        query: SQLAlchemy query object
        page (int): Номер страницы
        per_page (int): Количество элементов на странице

    Returns:
        dict: Данные с пагинацией
    """
    page = page or request.args.get('page', 1, type=int)
    per_page = min(per_page or request.args.get('per_page', 20, type=int), 100)

    paginated = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    }


def validate_user_permissions(required_role=None):
    """
    Декоратор для проверки прав пользователя

    Args:
        required_role (str): Требуемая роль пользователя
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
            from src.models.updated_models import User

            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                current_user = User.query.get(current_user_id)

                if not current_user:
                    return jsonify({'error': 'User not found'}), 404

                if required_role and current_user.role != required_role:
                    return jsonify({'error': 'Insufficient permissions'}), 403

                return f(current_user, *args, **kwargs)
            except Exception as e:
                logger.error(f"Permission validation error: {str(e)}")
                return jsonify({'error': 'Authentication required'}), 401
        return decorated_function
    return decorator


def format_api_response(data, message=None, status_code=200):
    """
    Стандартизированный формат ответа API

    Args:
        data: Данные для ответа
        message (str): Сообщение
        status_code (int): HTTP статус код

    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': 200 <= status_code < 300,
        'data': data
    }

    if message:
        response['message'] = message

    return jsonify(response), status_code
