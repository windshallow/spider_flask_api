# -*- coding: utf-8 -*-
from proj.projq.celery_app import app


@app.task
def add(x, y):
    return x + y