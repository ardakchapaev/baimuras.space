
# Gunicorn Configuration for Baimuras Production

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8001"
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
accesslog = "/home/ubuntu/baimuras-production/logs/access.log"
errorlog = "/home/ubuntu/baimuras-production/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "baimuras"

# Server mechanics
daemon = False
pidfile = "/home/ubuntu/baimuras-production/baimuras.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (if needed later)
# keyfile = None
# certfile = None

# Application
wsgi_module = "wsgi:app"
pythonpath = "/home/ubuntu/baimuras-production"

# Environment
raw_env = [
    "FLASK_ENV=production",
]
