# -*- coding: utf-8 -*-
"""
export FLASK_APP=hello.py
cd ~/funny/spider_flask_api/flask_learn     # 到hello.py文件所在目录
python -m flask run --host=0.0.0.0
"""
from flask import Flask, url_for, request

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello, World'


# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    print type(post_id), '=== show_post ==='
    return 'Post %d' % post_id


@app.route('/path/<path:sub_path>')
def show_sub_path(sub_path):
    # show the sub_path after /path/
    print type(sub_path), '=== show_sub_path ==='
    return 'Sub_path %s' % sub_path


@app.route('/projects/')  # 不规范，端点不以 / 结尾
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


# @app.route('/login')
# def login():
#     return 'login'


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)


with app.test_request_context():
    print url_for('index'), type(url_for('index'))
    # print url_for('login')
    # print url_for('login', next='/')
    print url_for('profile', username='John Doe')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def do_the_login():
    return 'do_the_login'


def show_the_login_form():
    return 'show_the_login_form'


