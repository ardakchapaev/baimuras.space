
# BaiMuras Website

Современный веб-сайт для мебельной студии BaiMuras с интеграцией n8n для автоматизации бизнес-процессов.

## Особенности

- **Основные страницы**: главная, о нас, услуги (мебель на заказ, дизайн-бюро, академия), портфолио, блог, контакты
- **Панель управления** с аутентификацией для управления лидами, аналитикой и настройками
- **REST API** для интеграции с n8n и внешними системами
- **Система лидов** с автоматическим скорингом и отслеживанием статусов
- **CSRF защита** для всех форм
- **Обработка ошибок** 404/500 с красивыми страницами
- **SEO оптимизация** с мета-тегами и структурированными данными

## Технологии

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, Jinja2 templates
- **База данных**: SQLite (разработка) / PostgreSQL (продакшен)
- **Безопасность**: Flask-WTF (CSRF), Werkzeug (хеширование паролей)
- **API**: Flask-CORS для интеграции с hub.baimuras.space

## Установка и настройка

### 1. Клонирование и установка зависимостей

```bash
git clone https://github.com/ardakchapaev/baimuras.space.git
cd baimuras.space
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Настройка окружения

Скопируйте файл с примером переменных окружения:
```bash
cp .env.sample .env
```

Отредактируйте `.env` файл:
```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///baimuras.db
API_KEY=your-api-key-for-n8n-integration
FLASK_ENV=development
```

### 3. Инициализация базы данных

```bash
python -c "from src.main import app; from src.models.user import db; app.app_context().push(); db.create_all()"
```

### 4. Запуск приложения

```bash
python wsgi.py
```

Сайт будет доступен по адресу: http://localhost:5000

## API Endpoints для n8n

### Webhooks (без API ключа)
- `POST /api/webhooks/contact` - Прием контактных форм

### Защищенные endpoints (требуют API ключ)
- `GET /api/leads` - Список всех лидов
- `GET /api/leads/<id>` - Получить конкретный лид
- `PUT /api/leads/<id>` - Обновить лид
- `POST /api/webhooks/lead` - Создать/обновить лид
- `GET /api/projects` - Список проектов
- `POST /api/projects` - Создать проект

### Аутентификация API
Добавьте заголовок: `X-API-Key: your-api-key`

## Интеграция с n8n

1. В n8n создайте HTTP Request узел
2. Укажите URL: `https://baimuras.space/api/webhooks/contact`
3. Метод: POST
4. Тело запроса (JSON):
```json
{
  "name": "Имя клиента",
  "email": "email@example.com",
  "phone": "+7 777 123 45 67",
  "subject": "Тема обращения",
  "message": "Текст сообщения",
  "source": "telegram"
}
```

## Деплой на Timeweb Cloud

### 1. Подготовка файлов

Создайте `runtime.txt`:
```
python-3.11
```

### 2. Настройка переменных окружения

В панели Timeweb Cloud установите:
- `SECRET_KEY` - секретный ключ (сгенерируйте надежный)
- `DATABASE_URL` - URL базы данных PostgreSQL
- `API_KEY` - ключ для API интеграции
- `FLASK_ENV=production`

### 3. Команды деплоя

```bash
pip install -r requirements.txt
python -c "from src.main import app; from src.models.user import db; app.app_context().push(); db.create_all()"
gunicorn --bind 0.0.0.0:8000 wsgi:application
```

## Структура проекта

```
baimuras.space/
├── src/
│   ├── models/          # Модели данных
│   │   ├── user.py      # Модель пользователя
│   │   ├── lead.py      # Модель лида
│   │   └── project.py   # Модель проекта
│   ├── routes/          # Маршруты
│   │   ├── main_routes.py  # Основные страницы
│   │   ├── user.py      # API пользователей
│   │   └── api.py       # API для n8n
│   ├── templates/       # HTML шаблоны
│   ├── static/          # CSS, JS, изображения
│   ├── config.py        # Конфигурация
│   ├── errors.py        # Обработчики ошибок
│   └── main.py          # Основное приложение
├── .env.sample          # Пример переменных окружения
├── requirements.txt     # Зависимости Python
├── wsgi.py             # WSGI точка входа
└── README.md           # Документация
```

## Безопасность

- ✅ SECRET_KEY из переменных окружения
- ✅ CSRF защита для всех форм
- ✅ Хеширование паролей с Werkzeug
- ✅ API ключи для защищенных endpoints
- ✅ CORS настроен только для hub.baimuras.space
- ✅ Валидация входных данных

## Поддержка

Для вопросов и предложений создавайте Issues в GitHub репозитории.
