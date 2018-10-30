# -*- coding: utf-8 -*-
from proj.celery_app import app


@app.task
def add(x, y):
    return x + y
