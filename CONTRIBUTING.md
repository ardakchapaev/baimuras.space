
# Руководство по участию в разработке - BaiMuras Platform

## Добро пожаловать!

Спасибо за интерес к проекту BaiMuras Platform! Это руководство поможет вам начать участие в разработке и следовать принятым стандартам.

## Кодекс поведения

Мы стремимся создать открытое и дружелюбное сообщество. Участвуя в проекте, вы соглашаетесь:

- **Быть уважительными** ко всем участникам
- **Конструктивно критиковать** код, а не людей
- **Помогать новичкам** и делиться знаниями
- **Следовать техническим стандартам** проекта

## Как начать

### 1. Настройка среды разработки

```bash
# Форк репозитория на GitHub
# Клонирование вашего форка
git clone https://github.com/YOUR_USERNAME/baimuras.space.git
cd baimuras.space

# Добавление upstream репозитория
git remote add upstream https://github.com/ardakchapaev/baimuras.space.git

# Переключение на рабочую ветку
git checkout fix-setup-env-1750496460

# Создание виртуального окружения
python3.11 -m venv venv
source venv/bin/activate

# Установка зависимостей для разработки
pip install -r requirements.txt
pip install pytest pytest-flask flake8 pylint bandit black isort
```

### 2. Настройка pre-commit хуков

```bash
# Установка pre-commit
pip install pre-commit

# Создание конфигурации pre-commit
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
EOF

# Установка хуков
pre-commit install
```

### 3. Настройка базы данных для разработки

```bash
# Создание тестовой базы данных
sudo -u postgres createdb baimuras_test

# Копирование переменных окружения
cp .env.example .env

# Редактирование .env для разработки
nano .env
```

## Стандарты разработки

### Структура кода

```
src/
├── models/          # Модели данных (SQLAlchemy)
├── routes/          # Маршруты и контроллеры
├── templates/       # HTML шаблоны (Jinja2)
├── static/          # Статические файлы
├── utils/           # Утилиты и хелперы
├── config.py        # Конфигурация приложения
└── main.py          # Точка входа приложения
```

### Соглашения по именованию

**Python код:**
- **Классы**: `PascalCase` (например, `UserModel`, `LeadManager`)
- **Функции и переменные**: `snake_case` (например, `get_user_by_id`, `user_email`)
- **Константы**: `UPPER_SNAKE_CASE` (например, `MAX_FILE_SIZE`, `DEFAULT_TIMEOUT`)
- **Приватные методы**: `_snake_case` (например, `_validate_email`)

**Файлы и директории:**
- **Python файлы**: `snake_case.py` (например, `user_model.py`, `email_utils.py`)
- **Шаблоны**: `snake_case.html` (например, `user_profile.html`)
- **Статические файлы**: `kebab-case` (например, `main-style.css`)

### Стиль кода

**Форматирование с Black:**
```bash
# Форматирование всего кода
black src/ tests/

# Проверка без изменений
black --check src/
```

**Сортировка импортов с isort:**
```bash
# Сортировка импортов
isort src/ tests/

# Проверка без изменений
isort --check-only src/
```

**Проверка стиля с Flake8:**
```bash
# Проверка стиля кода
flake8 src/ tests/
```

### Документация кода

**Docstrings для функций:**
```python
def create_user(email: str, name: str, role: str = "user") -> User:
    """
    Создает нового пользователя в системе.
    
    Args:
        email (str): Email адрес пользователя
        name (str): Полное имя пользователя
        role (str, optional): Роль пользователя. По умолчанию "user"
    
    Returns:
        User: Созданный объект пользователя
    
    Raises:
        ValidationError: Если email уже существует
        ValueError: Если переданы некорректные данные
    
    Example:
        >>> user = create_user("john@example.com", "John Doe", "admin")
        >>> print(user.email)
        john@example.com
    """
    # Реализация функции
    pass
```

**Docstrings для классов:**
```python
class LeadManager:
    """
    Менеджер для работы с лидами.
    
    Предоставляет методы для создания, обновления и управления лидами
    в CRM системе. Включает валидацию данных и интеграцию с n8n.
    
    Attributes:
        db_session: Сессия базы данных
        n8n_client: Клиент для интеграции с n8n
    
    Example:
        >>> manager = LeadManager(db_session)
        >>> lead = manager.create_lead("client@example.com", "John Doe")
    """
    
    def __init__(self, db_session):
        """
        Инициализация менеджера лидов.
        
        Args:
            db_session: Активная сессия базы данных
        """
        pass
```

## Процесс разработки

### Git Flow

Мы используем упрощенную версию Git Flow:

**Основные ветки:**
- `main` - стабильная продакшн версия
- `fix-setup-env-1750496460` - текущая рабочая ветка
- `feature/*` - ветки для новых функций
- `bugfix/*` - ветки для исправления багов
- `hotfix/*` - критические исправления для продакшн

### Создание новой функции

```bash
# Обновление рабочей ветки
git checkout fix-setup-env-1750496460
git pull upstream fix-setup-env-1750496460

# Создание ветки для новой функции
git checkout -b feature/user-profile-enhancement

# Разработка и коммиты
git add .
git commit -m "feat: add user profile photo upload"

# Отправка в ваш форк
git push origin feature/user-profile-enhancement
```

### Соглашения по коммитам

Мы используем [Conventional Commits](https://www.conventionalcommits.org/):

**Формат:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Типы коммитов:**
- `feat:` - новая функция
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование кода (без изменения логики)
- `refactor:` - рефакторинг кода
- `test:` - добавление или изменение тестов
- `chore:` - обновление зависимостей, конфигурации

**Примеры:**
```bash
git commit -m "feat(auth): add JWT token refresh functionality"
git commit -m "fix(api): resolve user creation validation error"
git commit -m "docs: update API documentation for leads endpoint"
git commit -m "test(models): add unit tests for User model"
```

### Pull Request процесс

1. **Создание PR:**
   - Убедитесь, что ваша ветка обновлена
   - Запустите все тесты локально
   - Создайте PR в основной репозиторий

2. **Шаблон PR:**
```markdown
## Описание изменений
Краткое описание того, что было изменено и почему.

## Тип изменений
- [ ] Исправление бага
- [ ] Новая функция
- [ ] Критическое изменение
- [ ] Обновление документации

## Тестирование
- [ ] Все существующие тесты проходят
- [ ] Добавлены новые тесты для новой функциональности
- [ ] Тестирование выполнено вручную

## Чеклист
- [ ] Код следует стандартам проекта
- [ ] Добавлены docstrings для новых функций
- [ ] Обновлена документация (если необходимо)
- [ ] Нет конфликтов с основной веткой
```

3. **Code Review:**
   - Ожидайте review от мейнтейнеров
   - Отвечайте на комментарии и вносите изменения
   - После одобрения PR будет смержен

## Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# Конкретный файл
pytest tests/test_api.py

# С покрытием кода
pytest --cov=src --cov-report=html

# Только быстрые тесты
pytest -m "not slow"
```

### Написание тестов

**Структура тестов:**
```
tests/
├── conftest.py          # Конфигурация pytest и фикстуры
├── test_models/         # Тесты моделей
├── test_routes/         # Тесты маршрутов
├── test_utils/          # Тесты утилит
└── test_integration/    # Интеграционные тесты
```

**Пример теста:**
```python
import pytest
from src.models.user import User
from src.utils.auth import create_user


class TestUserCreation:
    """Тесты создания пользователей."""
    
    def test_create_user_success(self, db_session):
        """Тест успешного создания пользователя."""
        # Arrange
        email = "test@example.com"
        name = "Test User"
        
        # Act
        user = create_user(email, name)
        
        # Assert
        assert user.email == email
        assert user.name == name
        assert user.role == "user"  # default role
        assert user.id is not None
    
    def test_create_user_duplicate_email(self, db_session):
        """Тест создания пользователя с существующим email."""
        # Arrange
        email = "duplicate@example.com"
        create_user(email, "First User")
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Email already exists"):
            create_user(email, "Second User")
```

### Фикстуры для тестов

```python
# tests/conftest.py
import pytest
from src import create_app
from src.models import db


@pytest.fixture
def app():
    """Создание тестового приложения."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Тестовый клиент Flask."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Сессия базы данных для тестов."""
    with app.app_context():
        yield db.session
```

## Качество кода

### Статический анализ

```bash
# Pylint - анализ качества кода
pylint src/

# Bandit - сканирование безопасности
bandit -r src/

# MyPy - проверка типов (если используется)
mypy src/
```

### Метрики качества

Мы стремимся поддерживать:
- **Pylint score**: 8.0+
- **Test coverage**: 80%+
- **Bandit**: без критических уязвимостей
- **Flake8**: без нарушений стиля

### Continuous Integration

При создании PR автоматически запускаются:
- Проверка стиля кода (Black, isort, Flake8)
- Статический анализ (Pylint, Bandit)
- Все тесты с покрытием кода
- Проверка безопасности зависимостей

## Документация

### Обновление документации

При добавлении новых функций обновляйте:
- **README.md** - если изменилась установка или основные функции
- **API.md** - для новых API эндпоинтов
- **ADMIN.md** - для изменений в админ-панели
- **Docstrings** - для всех новых функций и классов

### Стиль документации

- Используйте **Markdown** для всех документов
- Добавляйте **примеры кода** где это уместно
- Включайте **скриншоты** для UI изменений
- Поддерживайте **актуальность** ссылок и инструкций

## Безопасность

### Рекомендации по безопасности

1. **Никогда не коммитьте:**
   - Пароли и API ключи
   - Секретные токены
   - Персональные данные

2. **Всегда валидируйте:**
   - Пользовательский ввод
   - Параметры API
   - Загружаемые файлы

3. **Используйте:**
   - Параметризованные SQL запросы
   - CSRF токены для форм
   - Безопасные заголовки HTTP

### Сообщение об уязвимостях

Если вы обнаружили уязвимость безопасности:
1. **НЕ создавайте публичный Issue**
2. Отправьте email на: security@baimuras.space
3. Включите подробное описание и шаги воспроизведения
4. Мы ответим в течение 48 часов

## Релизы

### Процесс релиза

1. **Подготовка релиза:**
   - Обновление версии в `VERSION`
   - Обновление `CHANGELOG.md`
   - Финальное тестирование

2. **Создание релиза:**
   - Создание тега: `git tag v2.1.0`
   - Отправка тега: `git push origin v2.1.0`
   - Создание GitHub Release

3. **Развертывание:**
   - Автоматическое развертывание на staging
   - Ручное развертывание на продакшн
   - Мониторинг после развертывания

### Семантическое версионирование

Мы используем [SemVer](https://semver.org/):
- **MAJOR** (2.0.0) - breaking changes
- **MINOR** (2.1.0) - новые функции (обратно совместимые)
- **PATCH** (2.1.1) - исправления багов

## Сообщество

### Каналы связи

- **GitHub Issues** - баги и предложения функций
- **GitHub Discussions** - общие вопросы и обсуждения
- **Email** - admin@baimuras.space для прямой связи
- **Telegram** - @baimuras_dev (для разработчиков)

### Помощь новичкам

Ищите Issues с метками:
- `good first issue` - хорошие задачи для начинающих
- `help wanted` - нужна помощь сообщества
- `documentation` - улучшение документации

### Признание вклада

Все контрибьюторы упоминаются в:
- **CONTRIBUTORS.md** файле
- **GitHub Contributors** секции
- **Release notes** для значимых вкладов

## Часто задаваемые вопросы

### Q: Как настроить IDE для разработки?

**A:** Рекомендуемые настройки для VS Code:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true
}
```

### Q: Как запустить только определенные тесты?

**A:** Используйте pytest с фильтрами:
```bash
# Тесты конкретного модуля
pytest tests/test_models/test_user.py

# Тесты по имени
pytest -k "test_create_user"

# Тесты с определенной меткой
pytest -m "unit"
```

### Q: Как добавить новую зависимость?

**A:** 
1. Добавьте в `requirements.txt`
2. Установите: `pip install package_name`
3. Обновите requirements: `pip freeze > requirements.txt`
4. Протестируйте совместимость

### Q: Как обновить документацию API?

**A:** 
1. Обновите docstrings в коде
2. Добавьте примеры в `API.md`
3. Протестируйте все примеры
4. Обновите версию документации

## Благодарности

Спасибо всем, кто вносит вклад в развитие BaiMuras Platform! Ваши усилия помогают создавать лучший продукт для творческого сообщества.

### Основные контрибьюторы

- **Ardak Chapaev** - основатель и главный разработчик
- **Сообщество разработчиков** - за ценные предложения и исправления

---

**Последнее обновление**: 21 июня 2025 г.  
**Версия руководства**: 2.0.0

Если у вас есть вопросы по этому руководству, создайте Issue или свяжитесь с нами: admin@baimuras.space
