#!/bin/bash

# BaiMuras Platform Production Deployment Script
# Сервер: 95.140.153.181
# Домен: baimuras.space

set -e

echo "🚀 НАЧАЛО ДЕПЛОЯ ПЛАТФОРМЫ BAIMURAS"
echo "=================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для логирования
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Проверка переменных окружения
check_env() {
    log "Проверка переменных окружения..."
    
    if [ ! -f ".env.prod" ]; then
        error "Файл .env.prod не найден!"
    fi
    
    source .env.prod
    
    if [ -z "$POSTGRES_PASSWORD" ]; then
        error "POSTGRES_PASSWORD не установлен в .env.prod"
    fi
    
    if [ -z "$SECRET_KEY" ]; then
        error "SECRET_KEY не установлен в .env.prod"
    fi
    
    log "Переменные окружения проверены ✓"
}

# Создание необходимых директорий
create_directories() {
    log "Создание необходимых директорий..."
    
    mkdir -p uploads
    mkdir -p logs
    mkdir -p nginx/ssl
    mkdir -p backups
    mkdir -p static
    
    log "Директории созданы ✓"
}

# Проверка Docker
check_docker() {
    log "Проверка Docker..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker не установлен!"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose не установлен!"
    fi
    
    log "Docker проверен ✓"
}

# Остановка существующих контейнеров
stop_existing() {
    log "Остановка существующих контейнеров..."
    
    docker-compose -f docker-compose.prod.yml down --remove-orphans || true
    
    log "Существующие контейнеры остановлены ✓"
}

# Сборка образов
build_images() {
    log "Сборка Docker образов..."
    
    docker-compose -f docker-compose.prod.yml build --no-cache
    
    log "Образы собраны ✓"
}

# Запуск сервисов
start_services() {
    log "Запуск сервисов..."
    
    # Запуск базы данных и Redis
    docker-compose -f docker-compose.prod.yml up -d postgres redis
    
    # Ожидание готовности базы данных
    info "Ожидание готовности PostgreSQL..."
    sleep 30
    
    # Запуск Flask приложения
    docker-compose -f docker-compose.prod.yml up -d flask_app
    
    # Ожидание готовности Flask
    info "Ожидание готовности Flask..."
    sleep 20
    
    # Запуск админ панели
    docker-compose -f docker-compose.prod.yml up -d admin_panel
    
    # Запуск n8n
    docker-compose -f docker-compose.prod.yml up -d n8n
    
    # Запуск Nginx
    docker-compose -f docker-compose.prod.yml up -d nginx
    
    log "Все сервисы запущены ✓"
}

# Проверка здоровья сервисов
health_check() {
    log "Проверка здоровья сервисов..."
    
    # Проверка Flask API
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        log "Flask API работает ✓"
    else
        warning "Flask API недоступен"
    fi
    
    # Проверка Admin Panel
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log "Admin Panel работает ✓"
    else
        warning "Admin Panel недоступен"
    fi
    
    # Проверка n8n
    if curl -f http://localhost:5678 > /dev/null 2>&1; then
        log "n8n работает ✓"
    else
        warning "n8n недоступен"
    fi
}

# Создание бэкапа
create_backup() {
    log "Создание бэкапа..."
    
    BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_DIR="backups/backup_$BACKUP_DATE"
    
    mkdir -p "$BACKUP_DIR"
    
    # Бэкап базы данных
    docker exec baimuras_postgres pg_dump -U baimuras_user baimuras_db > "$BACKUP_DIR/database.sql"
    
    # Бэкап файлов
    tar -czf "$BACKUP_DIR/uploads.tar.gz" uploads/ || true
    tar -czf "$BACKUP_DIR/logs.tar.gz" logs/ || true
    
    log "Бэкап создан в $BACKUP_DIR ✓"
}

# Настройка SSL (Let's Encrypt)
setup_ssl() {
    log "Настройка SSL сертификатов..."
    
    if [ ! -f "nginx/ssl/baimuras.space.crt" ]; then
        warning "SSL сертификаты не найдены. Необходимо настроить Let's Encrypt вручную."
        info "Команды для настройки SSL:"
        info "1. Установите certbot: apt install certbot python3-certbot-nginx"
        info "2. Получите сертификат: certbot --nginx -d baimuras.space -d admin.baimuras.space -d api.baimuras.space -d n8n.baimuras.space"
    else
        log "SSL сертификаты найдены ✓"
    fi
}

# Показать статус
show_status() {
    log "Статус сервисов:"
    docker-compose -f docker-compose.prod.yml ps
    
    echo ""
    log "Доступные URL:"
    info "🌐 Основной сайт: https://baimuras.space"
    info "👨‍💼 Админ панель: https://admin.baimuras.space"
    info "🔧 API: https://api.baimuras.space"
    info "🤖 n8n: https://n8n.baimuras.space"
    
    echo ""
    log "Логи можно посмотреть командой:"
    info "docker-compose -f docker-compose.prod.yml logs -f [service_name]"
}

# Основная функция деплоя
main() {
    log "Начало деплоя BaiMuras Platform..."
    
    check_env
    create_directories
    check_docker
    stop_existing
    build_images
    start_services
    health_check
    create_backup
    setup_ssl
    show_status
    
    echo ""
    log "🎉 ДЕПЛОЙ ЗАВЕРШЕН УСПЕШНО!"
    log "Платформа BaiMuras готова к работе на baimuras.space"
}

# Запуск скрипта
main "$@"
