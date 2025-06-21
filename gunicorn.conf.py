"""Gunicorn configuration for BaiMuras application."""

import multiprocessing

# Server socket
BIND = "0.0.0.0:8000"
BACKLOG = 2048

# Worker processes
WORKERS = multiprocessing.cpu_count() * 2 + 1
WORKER_CLASS = "sync"
WORKER_CONNECTIONS = 1000
TIMEOUT = 30
KEEPALIVE = 2

# Restart workers
MAX_REQUESTS = 1000
MAX_REQUESTS_JITTER = 50

# Logging
LOGLEVEL = "info"
ACCESSLOG = "-"
ERRORLOG = "-"
ACCESS_LOG_FORMAT = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
PROC_NAME = "baimuras"

# Server mechanics
DAEMON = False
PIDFILE = "/tmp/gunicorn.pid"
USER = None
GROUP = None
TMP_UPLOAD_DIR = None

# SSL
KEYFILE = None
CERTFILE = None

# Application
WSGI_MODULE = "wsgi:application"
PYTHONPATH = "."
PRELOAD_APP = True

# Security
LIMIT_REQUEST_LINE = 4094
LIMIT_REQUEST_FIELDS = 100
LIMIT_REQUEST_FIELD_SIZE = 8190

# Performance
WORKER_TMP_DIR = "/dev/shm"
WORKER_CLASS = "sync"


def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    """Called just after a worker has been killed by a signal."""
    worker.log.info("worker received INT or QUIT signal")


def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def post_worker_init(worker):
    """Called just after a worker has initialized the application."""
    worker.log.info("Worker initialized (pid: %s)", worker.pid)


def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info("worker received SIGABRT signal")
