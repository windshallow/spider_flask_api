# -*- coding: utf-8 -*-
import sys
import os

from celery import Celery
from celery.task import task
import time

sys.path.insert(0, os.getcwd())
CELERY_IMPORTS = ("tasks", )
CELERY_RESULT_BACKEND = "amqp"
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')


@app.task()  # 生产任务到rabbitMQ中
def add(x, y):
    time.sleep(1)
    return x + y
