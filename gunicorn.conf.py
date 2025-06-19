
"""Gunicorn configuration for BaiMuras Platform.

This configuration provides production-ready settings for the Gunicorn WSGI server.
"""

import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
ACCESSLOG = "-"
ERRORLOG = "-"
LOGLEVEL = os.environ.get('LOG_LEVEL', 'info').lower()
ACCESS_LOG_FORMAT = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
PROC_NAME = 'baimuras_platform'

# Server mechanics
DAEMON = False
PIDFILE = '/tmp/gunicorn.pid'
USER = None
GROUP = None
TMP_UPLOAD_DIR = None

# Apply settings
accesslog = ACCESSLOG
errorlog = ERRORLOG
loglevel = LOGLEVEL
access_log_format = ACCESS_LOG_FORMAT
proc_name = PROC_NAME
daemon = DAEMON
pidfile = PIDFILE
user = USER
group = GROUP
tmp_upload_dir = TMP_UPLOAD_DIR

# SSL (uncomment and configure for HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Security
LIMIT_REQUEST_LINE = 4094
LIMIT_REQUEST_FIELDS = 100
LIMIT_REQUEST_FIELD_SIZE = 8190

# Application
WSGI_MODULE = "src.main:app"
PYTHONPATH = "."

# Preload application for better performance
PRELOAD_APP = True

# Apply settings
# pylint: disable=invalid-name
limit_request_line = LIMIT_REQUEST_LINE
# pylint: disable=invalid-name
limit_request_fields = LIMIT_REQUEST_FIELDS
# pylint: disable=invalid-name
limit_request_field_size = LIMIT_REQUEST_FIELD_SIZE
# pylint: disable=invalid-name
wsgi_module = WSGI_MODULE
# pylint: disable=invalid-name
pythonpath = PYTHONPATH
# pylint: disable=invalid-name
preload_app = PRELOAD_APP

# Worker lifecycle hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting BaiMuras Platform server")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading BaiMuras Platform server")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info(f"Worker {worker.pid} is being forked")

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"Worker {worker.pid} has been forked")

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info(f"Worker {worker.pid} received SIGABRT signal")
