# gunicorn.conf.py
import os
import multiprocessing

# conf
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))  # not for virtual machines
threads = int(os.getenv('GUNICORN_THREADS', 2))
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))
loglevel = os.getenv('GUNICORN_LOGLEVEL', 'info')

# Logs
accesslog = os.getenv('GUNICORN_ACCESSLOG', '-')  # logs in console
errorlog = os.getenv('GUNICORN_ERRORLOG', '-')    # error logs in console
