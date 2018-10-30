# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import Celery

app = Celery('spider_flask_api.proj', include=['spider_flask_api.proj.tasks'])
app.config_from_object('spider_flask_api.proj.celeryconfig')

if __name__ == '__main__':
    app.start()
