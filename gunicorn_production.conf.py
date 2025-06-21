"""
Production Gunicorn configuration for BaiMuras Platform
Оптимизированная конфигурация для продакшн среды
"""

import multiprocessing

# Основные настройки сервера
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Настройки процессов
preload_app = True
daemon = False
user = None
group = None
tmp_upload_dir = None

# Логирование
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Безопасность
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Производительность
worker_tmp_dir = "/dev/shm"
enable_stdio_inheritance = True

# SSL (если используется)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Мониторинг
pidfile = "logs/gunicorn.pid"
proc_name = "baimuras_platform"

# Хуки для логирования и мониторинга


def on_starting(server):
    """Вызывается при запуске сервера"""
    server.log.info("Starting BaiMuras Platform server")


def on_reload(server):
    """Вызывается при перезагрузке"""
    server.log.info("Reloading BaiMuras Platform server")


def when_ready(server):
    """Вызывается когда сервер готов принимать запросы"""
    server.log.info(
        "BaiMuras Platform server is ready. Listening on: %s", server.address
    )


def worker_int(worker):
    """Вызывается при получении SIGINT worker'ом"""
    worker.log.info("Worker received INT or QUIT signal")


def pre_fork(server, worker):
    """Вызывается перед fork worker'а"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def post_fork(server, worker):
    """Вызывается после fork worker'а"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def post_worker_init(worker):
    """Вызывается после инициализации worker'а"""
    worker.log.info("Worker initialized (pid: %s)", worker.pid)


def worker_abort(worker):
    """Вызывается при аварийном завершении worker'а"""
    worker.log.info("Worker aborted (pid: %s)", worker.pid)


def pre_exec(server):
    """Вызывается перед новым exec"""
    server.log.info("Forked child, re-executing.")


def pre_request(worker, req):
    """Вызывается перед обработкой запроса"""
    worker.log.debug("%s %s", req.method, req.path)


def post_request(worker, req, environ, resp):
    """Вызывается после обработки запроса"""
    worker.log.debug("%s %s - %s", req.method, req.path, resp.status_code)
