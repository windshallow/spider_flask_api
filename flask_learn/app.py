# -*- coding: utf-8 -*-
import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
# from flask.ext.mail import Mail, Message
from flask_mail import Mail, Message
from celery import Celery


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://guest@localhost//'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # redis
app.config['CELERY_RESULT_BACKEND'] = 'amqp://guest@localhost//'  # mq


# Initialize extensions
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    with app.app_context():
        mail.send(msg)


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index_2.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    msg = Message('Hello from Flask',
                  recipients=[request.form['email']])
    msg.body = 'This is a test email sent from a background Celery task.'
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(msg)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


# ----------------------------------------------- 通过 flask 的 /celery_test 接口调用celery 的 add 任务
# cd ~/Desktop/funny/spider_flask_api/flask_learn
# celery worker -A tasks.app -l INFO    开启worker，监听队列， -A参数指向 Celery类的实例的位置
# python app.py                         另开终端，同目录下启动flask服务
# 打开浏览器访问： http://127.0.0.1:5000/celery_test   即可触发celery任务

@celery.task
def add(x, y):
    return x + y


@app.route('/celery_test')
def celery_test():
    add.delay(4, 8)  # delay方法可触发任务 ！！！
    return 'starting'


# http://127.0.0.1:5000/calculate?x=3&y=4
@app.route('/calculate')
def calculate():
    x = int(request.args.get('x', 1))
    y = int(request.args.get('y', 1))
    res = add.delay(x, y)
    print res, type(res), dir(res)
    print res.result, type(res)  # 异步任务的结果是存在其他地方的，通常也不会用到结果值。【顶多成功与否发个信号】
    return 'starting calculate'


if __name__ == '__main__':
    app.run(debug=True)
