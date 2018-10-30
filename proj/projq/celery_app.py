# -*- coding: utf-8 -*-
from celery import Celery

app = Celery('proj.projq', include=['proj.projq.tasks'])
app.config_from_object('proj.projq.celeryconfig')

if __name__ == '__main__':
    app.start()
