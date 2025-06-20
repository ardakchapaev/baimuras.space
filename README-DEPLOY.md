# 🚀 Инструкция по деплою BaiMuras Platform

## 📋 Обзор

Данная инструкция описывает процесс деплоя полнофункциональной платформы BaiMuras на продакшн сервер.

## 🖥️ Информация о сервере

- **IP:** 95.140.153.181
- **Домен:** baimuras.space
- **SSH:** root/a78z2V*tCPV-g?
- **ОС:** Ubuntu/Debian (рекомендуется)

## 🏗️ Архитектура платформы

```
┌─────────────────────────────────────────────────────────────┐
│                    NGINX Reverse Proxy                     │
│                     (Port 80/443)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Flask API   │ │ Next.js     │ │ n8n         │
│ (Port 5000) │ │ Admin Panel │ │ Automation  │
│             │ │ (Port 3000) │ │ (Port 5678) │
└─────────────┘ └─────────────┘ └─────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ PostgreSQL  │ │ Redis       │ │ File        │
│ Database    │ │ Cache       │ │ Storage     │
│ (Port 5432) │ │ (Port 6379) │ │ (Volumes)   │
└─────────────┘ └─────────────┘ └─────────────┘
```

## 🔧 Компоненты системы

### Backend (Flask)
- **Порт:** 5000
- **Функции:** API, аутентификация, бизнес-логика
- **База данных:** PostgreSQL
- **Кеш:** Redis

### Frontend Admin (Next.js)
- **Порт:** 3000
- **Функции:** Админ панель, управление
- **Аутентификация:** NextAuth.js

### Автоматизация (n8n)
- **Порт:** 5678
- **Функции:** Workflow автоматизация
- **Интеграции:** Webhooks, API

### Reverse Proxy (Nginx)
- **Порты:** 80, 443
- **Функции:** SSL, балансировка, статика

## 📦 Предварительные требования

### На сервере должны быть установлены:

```bash
# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Git
sudo apt update && sudo apt install -y git

# Certbot для SSL
sudo apt install -y certbot python3-certbot-nginx
```

## 🚀 Процесс деплоя

### Шаг 1: Подключение к серверу

```bash
ssh root@95.140.153.181
# Пароль: a78z2V*tCPV-g?
```

### Шаг 2: Клонирование репозитория

```bash
cd /opt
git clone https://github.com/ardakchapaev/baimuras.space.git
cd baimuras.space
```

### Шаг 3: Настройка переменных окружения

```bash
# Скопировать и отредактировать файл окружения
cp .env.prod .env

# Отредактировать пароли и секретные ключи
nano .env
```

### Шаг 4: Запуск автоматического деплоя

```bash
# Сделать скрипт исполняемым
chmod +x deploy-production.sh

# Запустить деплой
./deploy-production.sh
```

### Шаг 5: Настройка DNS

Настройте A-записи для доменов:

```
baimuras.space          → 95.140.153.181
admin.baimuras.space    → 95.140.153.181
api.baimuras.space      → 95.140.153.181
n8n.baimuras.space      → 95.140.153.181
```

### Шаг 6: Настройка SSL

```bash
# Получение SSL сертификатов
certbot --nginx -d baimuras.space -d admin.baimuras.space -d api.baimuras.space -d n8n.baimuras.space

# Автоматическое обновление
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

## 🔍 Проверка работоспособности

### Проверка сервисов

```bash
# Статус всех контейнеров
docker-compose -f docker-compose.prod.yml ps

# Логи сервисов
docker-compose -f docker-compose.prod.yml logs -f flask_app
docker-compose -f docker-compose.prod.yml logs -f admin_panel
docker-compose -f docker-compose.prod.yml logs -f n8n
```

### Проверка доступности

```bash
# API
curl https://api.baimuras.space/health

# Admin Panel
curl https://admin.baimuras.space

# n8n
curl https://n8n.baimuras.space
```

## 🌐 Доступные URL

После успешного деплоя будут доступны:

- **🏠 Основной сайт:** https://baimuras.space
- **👨‍💼 Админ панель:** https://admin.baimuras.space
- **🔧 API:** https://api.baimuras.space
- **🤖 n8n Автоматизация:** https://n8n.baimuras.space

## 🔐 Учетные данные по умолчанию

### n8n
- **Пользователь:** admin
- **Пароль:** BaiMuras2025!n8nAdmin

### Admin Panel
- **Создается при первом запуске через регистрацию**

## 🛠️ Управление сервисами

### Основные команды

```bash
# Остановка всех сервисов
docker-compose -f docker-compose.prod.yml down

# Запуск всех сервисов
docker-compose -f docker-compose.prod.yml up -d

# Перезапуск конкретного сервиса
docker-compose -f docker-compose.prod.yml restart flask_app

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f [service_name]

# Обновление образов
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### Бэкапы

```bash
# Создание бэкапа базы данных
docker exec baimuras_postgres pg_dump -U baimuras_user baimuras_db > backup_$(date +%Y%m%d).sql

# Восстановление из бэкапа
docker exec -i baimuras_postgres psql -U baimuras_user baimuras_db < backup_file.sql
```

## 🚨 Устранение неполадок

### Проблемы с контейнерами

```bash
# Проверка статуса
docker ps -a

# Перезапуск проблемного контейнера
docker restart [container_name]

# Просмотр логов
docker logs [container_name]
```

### Проблемы с базой данных

```bash
# Подключение к базе данных
docker exec -it baimuras_postgres psql -U baimuras_user baimuras_db

# Проверка подключения
docker exec baimuras_postgres pg_isready -U baimuras_user
```

### Проблемы с SSL

```bash
# Проверка сертификатов
certbot certificates

# Обновление сертификатов
certbot renew

# Тест конфигурации Nginx
docker exec baimuras_nginx nginx -t
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи сервисов
2. Убедитесь в правильности DNS настроек
3. Проверьте доступность портов
4. Обратитесь к документации Docker и используемых сервисов

## 🔄 Обновление платформы

```bash
# Получение обновлений
git pull origin main

# Пересборка и перезапуск
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

---

**Дата создания:** 20 июня 2025  
**Версия:** 1.0  
**Статус:** Production Ready 🚀
