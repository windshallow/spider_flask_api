# -*- coding: utf-8 -*-
from __future__ import absolute_import
from proj.celery_app import app


@app.task
def add(x, y):
    return x + y
