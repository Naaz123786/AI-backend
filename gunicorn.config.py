#!/usr/bin/env python3
"""
Gunicorn configuration file to force uvicorn worker
"""
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"

# Worker processes
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"

# Worker connections
worker_connections = 1000

# Timeouts
timeout = 120
keepalive = 2

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"

# Process naming
proc_name = "ai-interview-backend"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
