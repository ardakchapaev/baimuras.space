
# 🎨 BaiMuras Platform - Профессиональная платформа мебельного инжиниринга

[![Python](https://i.ytimg.com/vi/4cgpu9L2AE8/maxresdefault.jpg)
[![Flask](https://i.ytimg.com/vi/qw3nRdcpZHw/maxresdefault.jpg)
[![PostgreSQL](https://i.ytimg.com/vi/uUalQbg-TGA/maxresdefault.jpg)
[![Redis](https://i.ytimg.com/vi/TFn9F2Fg0zg/maxresdefault.jpg)
[![License](https://miro.medium.com/v2/resize:fit:700/1*uw2XzJO65Li-qGEqoYzdmw.png)

> **Современная веб-платформа для мебельного дизайна с интегрированной CRM-системой, автоматизацией бизнес-процессов и админ-панелью**

## 🌟 Ключевые особенности

### 🎯 Основная платформа
- **Адаптивный дизайн**: Современный интерфейс с анимациями и плавными переходами
- **Портфолио проектов**: Оптимизированная галерея с lazy loading
- **Многоязычность**: Поддержка русского и казахского языков
- **SEO оптимизация**: Структурированные данные и meta теги
- **Контактные формы**: Валидация на клиенте и сервере

### 🛠️ CRM и Админ-панель
- **Управление лидами**: Полный цикл работы с потенциальными клиентами
- **Система проектов**: Отслеживание статуса и прогресса проектов
- **Аналитический дашборд**: Метрики и отчеты в реальном времени
- **Управление пользователями**: Ролевая система доступа
- **Консультации**: Планирование и управление встречами

### 🤖 Автоматизация
- **n8n интеграция**: Автоматизированные рабочие процессы
- **Celery задачи**: Фоновая обработка задач
- **Email уведомления**: Автоматическая отправка писем
- **Webhook система**: Интеграция с внешними сервисами
- **Backup автоматизация**: Регулярное резервное копирование

## 🚀 Быстрый старт

### Системные требования
- **Python**: 3.11 или выше
- **PostgreSQL**: 13 или выше  
- **Redis**: 6 или выше
- **Node.js**: 18+ (опционально, для фронтенд сборки)
- **Docker**: 20+ (для контейнеризации)

### Локальная установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/ardakchapaev/baimuras.space.git
cd baimuras.space
git checkout fix-setup-env-1750496460
```

2. **Создание виртуального окружения**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

4. **Настройка переменных окружения**
```bash
cp .env.example .env
# Отредактируйте .env файл согласно вашим настройкам
```

5. **Настройка базы данных**
```bash
# Создание базы данных PostgreSQL
createdb baimuras_db

# Инициализация миграций
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Запуск приложения**
```bash
# Режим разработки
python wsgi.py

# Или с Gunicorn (продакшн)
gunicorn -c gunicorn.conf.py wsgi:app
```

Приложение будет доступно по адресу: `http://localhost:5000`

### Docker установка

```bash
# Сборка и запуск всех сервисов
docker-compose up -d

# Только основное приложение
docker-compose up flask

# Просмотр логов
docker-compose logs -f flask
```

## 🏗️ Архитектура проекта

```
baimuras.space/
├── src/                          # Исходный код приложения
│   ├── __init__.py              # Инициализация Flask приложения
│   ├── main.py                  # Основная точка входа
│   ├── config.py                # Конфигурация приложения
│   ├── env_validator.py         # Валидация переменных окружения (НОВЫЙ)
│   ├── security_middleware.py   # Middleware безопасности (НОВЫЙ)
│   ├── secret_manager.py        # Управление секретами (НОВЫЙ)
│   ├── config_secure.py         # Безопасная конфигурация (НОВЫЙ)
│   ├── health_check.py          # Health check эндпоинты
│   ├── version.py               # Версионирование
│   ├── models/                  # Модели базы данных
│   │   ├── user.py             # Модель пользователя
│   │   ├── lead.py             # Модель лида
│   │   ├── project.py          # Модель проекта
│   │   ├── consultation.py     # Модель консультации
│   │   └── role.py             # Модель ролей
│   ├── routes/                  # Маршруты и контроллеры
│   │   ├── main_routes.py      # Основные маршруты
│   │   ├── api.py              # API эндпоинты
│   │   ├── api_v1.py           # API v1
│   │   ├── crm.py              # CRM функционал
│   │   ├── user.py             # Пользовательские маршруты
│   │   └── webhooks.py         # Webhook обработчики
│   ├── templates/               # HTML шаблоны
│   ├── static/                  # Статические файлы (CSS, JS, изображения)
│   ├── utils/                   # Утилиты и хелперы
│   │   ├── auth.py             # Аутентификация
│   │   ├── jwt_utils.py        # JWT утилиты
│   │   ├── logging_config.py   # Конфигурация логирования
│   │   ├── api_helpers.py      # API помощники
│   │   └── n8n.py              # n8n интеграция
│   └── automation/              # Celery задачи (перемещено в src)
│       ├── __init__.py
│       └── tasks/              # Задачи автоматизации
│           ├── email_tasks.py
│           └── notification_tasks.py
├── migrations/                  # Миграции базы данных
├── tests/                       # Тесты
├── nginx/                       # Конфигурация Nginx
├── docker-compose.yml          # Docker Compose конфигурация
├── requirements.txt            # Python зависимости
├── wsgi.py                     # WSGI точка входа
├── app.py                      # Основное приложение Flask
├── run_modernized.py           # Модернизированный запуск
└── gunicorn.conf.py           # Конфигурация Gunicorn
```

## 🌐 Развертывание

### Продакшн окружение
- **Основной сайт**: https://baimuras.space
- **Админ-панель**: https://hub.baimuras.space  
- **Автоматизация**: https://automation.baimuras.space
- **Сервер**: 95.140.153.181

### Доступы для разработки
```bash
# База данных
Host: localhost
Database: baimuras_db
User: baimuras_user
Password: BaiMuras2025!@#

# Redis
Host: localhost:6379
Password: baimuras2025

# n8n (автоматизация)
URL: http://localhost:5678
User: admin@baimuras.space
Password: Admin123!
```

Подробные инструкции по развертыванию см. в [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🔒 Безопасность

### Реализованные меры
- ✅ **Input Validation**: Валидация всех пользовательских данных
- ✅ **XSS Protection**: Защита от межсайтового скриптинга  
- ✅ **SQL Injection**: Параметризованные запросы ORM
- ✅ **CSRF Protection**: Токены защиты от подделки запросов
- ✅ **Rate Limiting**: Ограничение частоты запросов
- ✅ **Secure Headers**: Настройка безопасных HTTP заголовков
- ✅ **Session Security**: Безопасное управление сессиями
- ✅ **JWT Authentication**: Токены доступа для API

### Аудит безопасности
- **Pylint Score**: 8.53/10 (улучшен с 8.37)
- **Bandit Scan**: Все критические уязвимости устранены
- **Dependencies**: Актуальные версии без известных уязвимостей
- **Environment Validation**: Автоматическая валидация переменных окружения
- **Secret Management**: Удален хардкод секретов, добавлена валидация ключей

Подробнее см. [SECURITY.md](./SECURITY.md)

## 📊 API Документация

### Основные эндпоинты

**Публичные маршруты:**
- `GET /` - Главная страница
- `GET /about` - О компании
- `GET /services` - Услуги
- `GET /portfolio` - Портфолио
- `POST /contact` - Контактная форма
- `POST /api/consultation` - Запрос консультации

**API v1 (требует аутентификации):**
- `POST /api/v1/auth/login` - Вход в систему
- `GET /api/v1/users` - Список пользователей
- `GET /api/v1/leads` - Список лидов
- `POST /api/v1/leads` - Создание лида

**Webhook эндпоинты:**
- `POST /webhooks/n8n` - n8n webhook
- `POST /webhooks/lead-automation` - Автоматизация лидов
- `POST /webhooks/consultation-reminder` - Напоминания о консультациях

Полная документация API: [API.md](./API.md)

## 🛠️ Разработка

### Настройка среды разработки
```bash
# Установка зависимостей для разработки
pip install pytest pytest-flask flake8 pylint bandit

# Настройка переменных окружения
export FLASK_ENV=development
export FLASK_DEBUG=1

# Запуск в режиме разработки
python wsgi.py
```

### Запуск тестов
```bash
# Все тесты
python -m pytest

# С покрытием кода
python -m pytest --cov=src --cov-report=html

# Конкретный тест
python -m pytest tests/test_api.py::test_health_check
```

### Проверка качества кода
```bash
# Статический анализ
pylint src/

# Проверка стиля
flake8 src/

# Сканирование безопасности
bandit -r src/
```

## 🔧 Конфигурация

### Основные переменные окружения

| Переменная | Описание | Обязательная | Пример |
|------------|----------|--------------|---------|
| `SECRET_KEY` | Секретный ключ Flask (мин. 32 символа) | ✅ | `your-very-long-secret-key-here` |
| `JWT_SECRET_KEY` | Секретный ключ JWT (мин. 32 символа) | ✅ | `your-jwt-secret-key-here` |
| `DATABASE_TYPE` | Тип базы данных | ❌ | `sqlite` или `postgresql` |
| `DATABASE_PATH` | Путь к базе SQLite | ❌ | `instance/baimuras.db` |
| `REDIS_HOST` | Хост Redis сервера | ❌ | `localhost` |
| `REDIS_PORT` | Порт Redis сервера | ❌ | `6379` |
| `REDIS_DB` | Номер базы Redis | ❌ | `0` |
| `MAIL_SERVER` | SMTP сервер | ❌ | `smtp.gmail.com` |
| `MAIL_USERNAME` | Пользователь SMTP | ❌ | `user@gmail.com` |
| `MAIL_PASSWORD` | Пароль SMTP | ❌ | `app-password` |
| `N8N_WEBHOOK_URL` | URL webhook n8n | ❌ | `http://localhost:5678/webhook/baimuras` |
| `FLASK_ENV` | Окружение Flask | ❌ | `development` или `production` |
| `LOG_LEVEL` | Уровень логирования | ❌ | `INFO`, `DEBUG`, `ERROR` |

**Примечание**: Переменные с ✅ обязательны для запуска. Система автоматически проверяет их наличие при старте.

Полный список переменных см. в [.env.example](./.env.example)

## 📈 Мониторинг

### Health Check эндпоинты
- `GET /health` - Статус приложения
- `GET /api/health` - Статус API
- `GET /webhooks/health` - Статус webhook системы

### Логирование
```bash
# Логи приложения
tail -f logs/baimuras.log

# Логи ошибок
tail -f logs/error.log

# Логи Nginx (продакшн)
tail -f /var/log/nginx/baimuras_access.log
```

## 🧪 Тестирование

### Структура тестов
```
tests/
├── conftest.py              # Конфигурация pytest
├── test_api.py             # Тесты API
├── test_integration.py     # Интеграционные тесты
└── test_webhook.py         # Тесты webhook
```

### Запуск тестов
```bash
# Все тесты
pytest

# Конкретная категория
pytest tests/test_api.py

# С детальным выводом
pytest -v --tb=short
```

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature ветку: `git checkout -b feature/amazing-feature`
3. Commit изменения: `git commit -m 'Add amazing feature'`
4. Push в ветку: `git push origin feature/amazing-feature`
5. Создайте Pull Request

См. [CONTRIBUTING.md](./CONTRIBUTING.md) для подробных правил разработки.

## 📄 Лицензия

Проект лицензирован под MIT License - см. [LICENSE](./LICENSE) для деталей.

## 👨‍💻 Автор

**Ardak Chapaev**
- GitHub: [@ardakchapaev](https://github.com/ardakchapaev)
- Email: admin@baimuras.space
- Website: [baimuras.space](https://baimuras.space)

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте существующие [Issues](https://github.com/ardakchapaev/baimuras.space/issues)
2. Создайте новый Issue с подробным описанием
3. Свяжитесь с автором: admin@baimuras.space

## 🙏 Благодарности

- Flask команде за отличный фреймворк
- Сообществу разработчиков за вклад в open source
- Всем тестировщикам и контрибьюторам проекта

---

<div align="center">
  <strong>Сделано с ❤️ для творческого сообщества Казахстана</strong>
</div>
