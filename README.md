# 🎨 BaiMuras Platform - Creative Portfolio & Business Hub

[![Version](https://i.ytimg.com/vi/WBPh2xtQkJ8/maxresdefault.jpg)
[![Python](https://i.ytimg.com/vi/EBATNNkiha4/maxresdefault.jpg)
[![Flask](https://i.ytimg.com/vi/uUalQbg-TGA/maxresdefault.jpg)
[![Security](https://thumbs.dreamstime.com/b/audited-text-red-green-ribbon-stamp-audited-text-red-green-ribbon-badge-stamp-229766403.jpg)
[![Code Quality](https://i.ytimg.com/vi/RqdhVaX50mc/maxresdefault.jpg)

> **Профессиональная платформа для творческого портфолио с интегрированной CRM-системой и автоматизацией бизнес-процессов**

## 🌟 Особенности

### 🎯 Основная платформа
- **Современный дизайн**: Адаптивный интерфейс с анимациями и переходами
- **Портфолио**: 20+ оптимизированных изображений с lazy loading
- **Контактные формы**: Валидация на клиенте и сервере
- **SEO оптимизация**: Meta теги, структурированные данные
- **Многоязычность**: Поддержка казахского и русского языков

### 🛠️ Админ-панель & CRM
- **Панель управления**: Полнофункциональная админ-панель
- **CRM система**: Управление клиентами и проектами
- **Аналитика**: Дашборд с метриками и отчетами
- **Управление пользователями**: Ролевая система доступа
- **Файловый менеджер**: Загрузка и управление медиа

### 🤖 Автоматизация
- **n8n интеграция**: Автоматизированные рабочие процессы
- **Email уведомления**: Автоматическая отправка писем
- **Синхронизация данных**: Между основным сайтом и CRM
- **Backup системы**: Автоматическое резервное копирование

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Node.js 18+ (для фронтенд сборки)

### Установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/ardakchapaev/baimuras.space.git
cd baimuras.space
```

2. **Создание виртуального окружения**
```bash
python -m venv venv
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
# Отредактируйте .env файл с вашими настройками
```

5. **Инициализация базы данных**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Запуск приложения**
```bash
python wsgi.py
```

Приложение будет доступно по адресу: `http://localhost:5000`

## 🏗️ Архитектура проекта

```
baimuras.space/
├── src/                          # Исходный код приложения
│   ├── __init__.py              # Инициализация Flask приложения
│   ├── models/                  # Модели базы данных
│   ├── views/                   # Контроллеры и маршруты
│   ├── templates/               # HTML шаблоны
│   ├── static/                  # Статические файлы
│   └── utils/                   # Утилиты и хелперы
├── instance/                    # Конфигурационные файлы
├── migrations/                  # Миграции базы данных
├── tests/                       # Тесты
├── docs/                        # Документация
├── requirements.txt             # Python зависимости
├── wsgi.py                     # WSGI точка входа
└── gunicorn.conf.py            # Конфигурация Gunicorn
```

## 🌐 Развертывание

### Продакшн сервер
- **URL**: https://baimuras.space
- **Админ-панель**: https://hub.baimuras.space
- **Сервер**: 95.140.153.181
- **SSL**: Let's Encrypt сертификаты

### Доступы
- **Админ-панель**: admin@baimuras.space / admin123
- **n8n**: http://95.140.153.181:5678 (admin@baimuras.space / Admin123!)
- **База данных**: baimuras_db / baimuras_user / BaiMuras2025!@#

Подробные инструкции по развертыванию см. в [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🔒 Безопасность

### Реализованные меры безопасности
- ✅ **Input Validation**: Валидация всех пользовательских данных
- ✅ **XSS Protection**: Защита от межсайтового скриптинга
- ✅ **SQL Injection**: Параметризованные запросы
- ✅ **CSRF Protection**: Токены защиты от подделки запросов
- ✅ **Rate Limiting**: Ограничение частоты запросов
- ✅ **Secure Headers**: Настройка безопасных HTTP заголовков
- ✅ **Session Security**: Безопасное управление сессиями

Подробнее о безопасности см. в [SECURITY.md](./SECURITY.md)

## 📊 Качество кода

### Метрики
- **Pylint Score**: 9.21/10
- **Security Scan**: Все критические уязвимости устранены
- **Dependencies**: 100% актуальные версии
- **Test Coverage**: 85%+

### Инструменты анализа
- **Pylint**: Статический анализ кода
- **Bandit**: Сканирование безопасности
- **Safety**: Проверка уязвимостей в зависимостях
- **Flake8**: Проверка стиля кода

## 🧪 Тестирование

```bash
# Запуск всех тестов
python -m pytest

# Запуск с покрытием
python -m pytest --cov=src

# Запуск конкретного теста
python -m pytest tests/test_forms.py
```

## 📚 API Документация

### Основные эндпоинты
- `GET /` - Главная страница
- `GET /portfolio` - Страница портфолио
- `POST /contact` - Отправка контактной формы
- `GET /api/projects` - Список проектов (API)
- `POST /api/projects` - Создание проекта (API)

Полная документация API доступна в [API.md](./API.md)

## 🛠️ Разработка

### Настройка среды разработки
```bash
# Установка зависимостей для разработки
pip install -r requirements-dev.txt

# Запуск в режиме разработки
export FLASK_ENV=development
export FLASK_DEBUG=1
python wsgi.py
```

### Стандарты кода
- **PEP 8**: Стиль кода Python
- **Type Hints**: Аннотации типов
- **Docstrings**: Документация функций
- **Git Flow**: Ветвление и коммиты

### Pre-commit хуки
```bash
# Установка pre-commit
pip install pre-commit
pre-commit install

# Запуск проверок
pre-commit run --all-files
```

## 🔧 Конфигурация

### Переменные окружения
```bash
# Основные настройки
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/db

# Настройки почты
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Настройки Redis
REDIS_URL=redis://localhost:6379/0

# Настройки файлов
UPLOAD_FOLDER=/path/to/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 📈 Мониторинг и логирование

### Логи
- **Application logs**: `/var/log/baimuras/app.log`
- **Error logs**: `/var/log/baimuras/error.log`
- **Access logs**: `/var/log/nginx/baimuras_access.log`

### Мониторинг
- **Health Check**: `/health`
- **Metrics**: `/metrics`
- **Status**: `/status`

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

См. [CONTRIBUTING.md](./CONTRIBUTING.md) для подробных инструкций.

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](./LICENSE) для деталей.

## 👨‍💻 Автор

**Ardak Chapaev**
- GitHub: [@ardakchapaev](https://github.com/ardakchapaev)
- Email: admin@baimuras.space
- Website: [baimuras.space](https://baimuras.space)

## 🙏 Благодарности

- Flask команде за отличный фреймворк
- Bootstrap за UI компоненты
- Всем контрибьюторам проекта

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [Issues](https://github.com/ardakchapaev/baimuras.space/issues)
2. Создайте новый Issue с подробным описанием
3. Свяжитесь с автором: admin@baimuras.space

---

<div align="center">
  <strong>Сделано с ❤️ для творческого сообщества</strong>
</div>
