#!/bin/bash

# Скрипт деплоя BaiMuras Platform на сервер 95.140.153.181
# Использование: ./deploy.sh [environment]

set -e  # Остановка при ошибке

# Конфигурация
SERVER_IP="95.140.153.181"
SERVER_USER="root"
DOMAIN="baimuras.space"
ADMIN_DOMAIN="hub.baimuras.space"
AUTOMATION_DOMAIN="automation.baimuras.space"
DEPLOY_PATH="/opt/baimuras"
BACKUP_PATH="/opt/baimuras/backups"
ENVIRONMENT="${1:-production}"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для вывода
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка зависимостей
check_dependencies() {
    log_info "Проверка зависимостей..."
    
    if ! command -v rsync &> /dev/null; then
        log_error "rsync не установлен. Установите: sudo apt install rsync"
        exit 1
    fi
    
    if ! command -v ssh &> /dev/null; then
        log_error "ssh не установлен"
        exit 1
    fi
    
    log_success "Все зависимости установлены"
}

# Проверка подключения к серверу
check_server_connection() {
    log_info "Проверка подключения к серверу $SERVER_IP..."
    
    if ! ssh -o ConnectTimeout=10 -o BatchMode=yes $SERVER_USER@$SERVER_IP exit 2>/dev/null; then
        log_error "Не удается подключиться к серверу $SERVER_IP"
        log_info "Убедитесь, что:"
        log_info "1. SSH ключ добавлен на сервер"
        log_info "2. Сервер доступен"
        log_info "3. Пользователь $SERVER_USER существует"
        exit 1
    fi
    
    log_success "Подключение к серверу установлено"
}

# Создание резервной копии
create_backup() {
    log_info "Создание резервной копии..."
    
    BACKUP_NAME="baimuras_backup_$(date +%Y%m%d_%H%M%S)"
    
    ssh $SERVER_USER@$SERVER_IP "
        mkdir -p $BACKUP_PATH
        if [ -d $DEPLOY_PATH ]; then
            tar -czf $BACKUP_PATH/$BACKUP_NAME.tar.gz -C $DEPLOY_PATH .
            echo 'Резервная копия создана: $BACKUP_PATH/$BACKUP_NAME.tar.gz'
        else
            echo 'Директория $DEPLOY_PATH не существует, пропускаем резервное копирование'
        fi
    "
    
    log_success "Резервная копия создана"
}

# Подготовка сервера
prepare_server() {
    log_info "Подготовка сервера..."
    
    ssh $SERVER_USER@$SERVER_IP "
        # Обновление системы
        apt update && apt upgrade -y
        
        # Установка Docker
        if ! command -v docker &> /dev/null; then
            curl -fsSL https://get.docker.com -o get-docker.sh
            sh get-docker.sh
            systemctl enable docker
            systemctl start docker
        fi
        
        # Установка Docker Compose
        if ! command -v docker-compose &> /dev/null; then
            curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose
            chmod +x /usr/local/bin/docker-compose
        fi
        
        # Установка других зависимостей
        apt install -y nginx certbot python3-certbot-nginx ufw fail2ban
        
        # Создание директорий
        mkdir -p $DEPLOY_PATH
        mkdir -p $BACKUP_PATH
        mkdir -p /var/log/baimuras
        
        # Настройка firewall
        ufw --force enable
        ufw allow ssh
        ufw allow http
        ufw allow https
        
        echo 'Сервер подготовлен'
    "
    
    log_success "Сервер подготовлен"
}

# Синхронизация файлов
sync_files() {
    log_info "Синхронизация файлов с сервером..."
    
    # Исключения для rsync
    cat > .rsyncignore << EOF
.git/
.gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.DS_Store
.vscode/
.idea/
*.swp
*.swo
*~
.rsyncignore
node_modules/
.env
instance/
logs/
uploads/
EOF
    
    # Синхронизация кода
    rsync -avz --delete --exclude-from=.rsyncignore \
        ./ $SERVER_USER@$SERVER_IP:$DEPLOY_PATH/
    
    # Удаление временного файла
    rm .rsyncignore
    
    log_success "Файлы синхронизированы"
}

# Настройка переменных окружения
setup_environment() {
    log_info "Настройка переменных окружения..."
    
    ssh $SERVER_USER@$SERVER_IP "
        cd $DEPLOY_PATH
        
        # Создание .env файла если не существует
        if [ ! -f .env ]; then
            cp .env.example .env
            
            # Генерация секретных ключей
            SECRET_KEY=\$(openssl rand -hex 32)
            JWT_SECRET_KEY=\$(openssl rand -hex 32)
            N8N_WEBHOOK_SECRET=\$(openssl rand -hex 16)
            
            # Обновление .env файла
            sed -i \"s/your-secret-key-change-in-production/\$SECRET_KEY/g\" .env
            sed -i \"s/your-jwt-secret-key-change-in-production/\$JWT_SECRET_KEY/g\" .env
            sed -i \"s/your-webhook-secret/\$N8N_WEBHOOK_SECRET/g\" .env
            sed -i \"s/FLASK_ENV=development/FLASK_ENV=$ENVIRONMENT/g\" .env
            
            echo 'Файл .env создан с безопасными ключами'
        else
            echo 'Файл .env уже существует'
        fi
        
        # Создание необходимых директорий
        mkdir -p uploads logs instance nginx/ssl
        chmod 755 uploads logs instance
    "
    
    log_success "Переменные окружения настроены"
}

# Запуск приложения
start_application() {
    log_info "Запуск приложения..."
    
    ssh $SERVER_USER@$SERVER_IP "
        cd $DEPLOY_PATH
        
        # Остановка существующих контейнеров
        docker-compose down || true
        
        # Сборка и запуск новых контейнеров
        docker-compose build --no-cache
        docker-compose up -d
        
        # Ожидание запуска сервисов
        echo 'Ожидание запуска сервисов...'
        sleep 30
        
        # Проверка статуса
        docker-compose ps
    "
    
    log_success "Приложение запущено"
}

# Настройка Nginx
setup_nginx() {
    log_info "Настройка Nginx..."
    
    ssh $SERVER_USER@$SERVER_IP "
        # Копирование конфигурации Nginx
        cp $DEPLOY_PATH/nginx/nginx.conf /etc/nginx/nginx.conf
        
        # Создание конфигурации сайтов
        cat > /etc/nginx/sites-available/baimuras << 'EOF'
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

server {
    listen 80;
    server_name $ADMIN_DOMAIN;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

server {
    listen 80;
    server_name $AUTOMATION_DOMAIN;
    
    location / {
        proxy_pass http://localhost:5678;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket поддержка
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \"upgrade\";
    }
}
EOF
        
        # Активация сайта
        ln -sf /etc/nginx/sites-available/baimuras /etc/nginx/sites-enabled/
        rm -f /etc/nginx/sites-enabled/default
        
        # Проверка конфигурации
        nginx -t
        
        # Перезапуск Nginx
        systemctl restart nginx
        systemctl enable nginx
    "
    
    log_success "Nginx настроен"
}

# Настройка SSL сертификатов
setup_ssl() {
    log_info "Настройка SSL сертификатов..."
    
    ssh $SERVER_USER@$SERVER_IP "
        # Получение SSL сертификатов
        certbot --nginx -d $DOMAIN -d www.$DOMAIN -d $ADMIN_DOMAIN -d $AUTOMATION_DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
        
        # Настройка автоматического обновления
        echo '0 12 * * * /usr/bin/certbot renew --quiet' | crontab -
    "
    
    log_success "SSL сертификаты настроены"
}

# Инициализация базы данных
init_database() {
    log_info "Инициализация базы данных..."
    
    ssh $SERVER_USER@$SERVER_IP "
        cd $DEPLOY_PATH
        
        # Ожидание запуска базы данных
        echo 'Ожидание запуска базы данных...'
        sleep 10
        
        # Выполнение миграций
        docker-compose exec -T web flask db upgrade || echo 'Миграции не выполнены (возможно, база уже инициализирована)'
        
        # Создание начальных данных
        docker-compose exec -T web python -c \"
from src.main import create_app
from src.models import db, Role, User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Создание ролей
    if not Role.query.filter_by(name='admin').first():
        admin_role = Role(name='admin', description='Administrator')
        manager_role = Role(name='manager', description='Manager')
        user_role = Role(name='user', description='User')
        
        db.session.add(admin_role)
        db.session.add(manager_role)
        db.session.add(user_role)
        
        # Создание администратора
        admin_user = User(
            email='admin@baimuras.space',
            name='Administrator',
            role=admin_role
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        print('Начальные данные созданы')
        print('Администратор: admin@baimuras.space / admin123')
    else:
        print('Начальные данные уже существуют')
\"
    "
    
    log_success "База данных инициализирована"
}

# Проверка работоспособности
health_check() {
    log_info "Проверка работоспособности..."
    
    # Проверка основного сайта
    if curl -f -s http://$DOMAIN/api/health > /dev/null; then
        log_success "Основной сайт работает: http://$DOMAIN"
    else
        log_warning "Основной сайт недоступен: http://$DOMAIN"
    fi
    
    # Проверка админ панели
    if curl -f -s http://$ADMIN_DOMAIN > /dev/null; then
        log_success "Админ панель работает: http://$ADMIN_DOMAIN"
    else
        log_warning "Админ панель недоступна: http://$ADMIN_DOMAIN"
    fi
    
    # Проверка n8n
    if curl -f -s http://$AUTOMATION_DOMAIN > /dev/null; then
        log_success "n8n работает: http://$AUTOMATION_DOMAIN"
    else
        log_warning "n8n недоступен: http://$AUTOMATION_DOMAIN"
    fi
    
    # Проверка сервисов на сервере
    ssh $SERVER_USER@$SERVER_IP "
        cd $DEPLOY_PATH
        echo 'Статус Docker контейнеров:'
        docker-compose ps
        
        echo ''
        echo 'Логи приложения (последние 20 строк):'
        docker-compose logs --tail=20 web
    "
}

# Показ информации о деплое
show_deploy_info() {
    log_success "Деплой завершен успешно!"
    echo ""
    echo "🌐 Доступные URL:"
    echo "   Основной сайт: http://$DOMAIN"
    echo "   Админ панель:  http://$ADMIN_DOMAIN"
    echo "   Автоматизация: http://$AUTOMATION_DOMAIN"
    echo ""
    echo "🔐 Доступы:"
    echo "   Администратор: admin@baimuras.space / admin123"
    echo "   n8n:          admin / baimuras2025"
    echo ""
    echo "📁 Пути на сервере:"
    echo "   Приложение: $DEPLOY_PATH"
    echo "   Резервные копии: $BACKUP_PATH"
    echo "   Логи: /var/log/baimuras"
    echo ""
    echo "🔧 Полезные команды:"
    echo "   Просмотр логов: ssh $SERVER_USER@$SERVER_IP 'cd $DEPLOY_PATH && docker-compose logs -f'"
    echo "   Перезапуск: ssh $SERVER_USER@$SERVER_IP 'cd $DEPLOY_PATH && docker-compose restart'"
    echo "   Остановка: ssh $SERVER_USER@$SERVER_IP 'cd $DEPLOY_PATH && docker-compose down'"
}

# Основная функция деплоя
main() {
    log_info "Начало деплоя BaiMuras Platform на $SERVER_IP"
    log_info "Окружение: $ENVIRONMENT"
    echo ""
    
    check_dependencies
    check_server_connection
    create_backup
    prepare_server
    sync_files
    setup_environment
    start_application
    setup_nginx
    init_database
    
    # SSL только для продакшена
    if [ "$ENVIRONMENT" = "production" ]; then
        setup_ssl
    fi
    
    health_check
    show_deploy_info
}

# Обработка ошибок
trap 'log_error "Деплой прерван из-за ошибки"; exit 1' ERR

# Запуск основной функции
main "$@"
