from dotenv import load_dotenv
import os
import multiprocessing

load_dotenv()

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'
reload = True

loglevel = os.environ.get('LOG_LEVEL', 'info')
accesslog = '-'
errorlog = '-'

timeout = 60
graceful_timeout = 15
keepalive = 5
worker_timeout = 60
max_requests = 1000
max_requests_jitter = 50
max_request_jitter = 100
start_class = "gunicorn.workers.ggevent.GeventWorker"
preload_app = True
daemon = False
pidfile = '/var/run/gunicorn.pid'
proc_name = 'openai_api_client'
raw_env = ["OPENAI_API_KEY=" + os.environ["OPENAI_API_KEY"],
           "DATABASE_URL=" + os.environ["DATABASE_URL"],
           "SECRET_KEY=" + os.environ["SECRET_KEY"],
           "LOG_LEVEL=" + os.environ["LOG_LEVEL"]]