# -*- coding: utf-8 -*-
"""
export FLASK_APP=hello.py
cd ~/funny/spider_flask_api/flask_learn     # 到hello.py文件所在目录
python -m flask run --host=0.0.0.0
"""
from flask import Flask, url_for, request, render_template, redirect, abort, make_response, session, escape, flash

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


@app.route('/')
def index():
    return 'Index Page'


# @app.route('/hello')
# def hello():
#     return 'Hello, World'


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

    string = """  
    projects 的URL是中规中举的，尾部有一个斜杠，看起来就如同一个文件夹。 
    访问一个没有斜杠结尾的URL时，Flask会自动进行重定向，帮你在尾部加上一个斜杠。
    """
    # return 'The project page'
    return string


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


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)  # 只要templates目录在你的flask app 同级目录下，模板就可以被找到。


# 在做单元测试时用, 测试某个接口请求等等
with app.test_request_context('/login', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    print '=== Test ==='
    assert request.path == '/login'
    assert request.method == 'POST'
    print request


# -------------------------  登陆以及验证的简单模拟  -------------------------


@app.route('/login_2', methods=['POST', 'GET'])
def login_2():
    """
    http://127.0.0.1:5000/login_2?username=lrw&password=123456

    """
    name = request.cookies.get('name')  # 访问 cookies
    print 'cookies: name: ', name

    # error = None
    error = 'error'

    if request.method == 'POST':

        # username = request.form['username']  # 表单提交的参数用 form 来获取
        # password = request.form['password']

        username = request.args.get('username')  # 要操作 URL （如 ?key=value ）中提交的参数可以使用 args 属性
        password = request.args.get('password')  # 我们推荐使用 get 或通过捕捉 KeyError 来访问 URL 参数, 而不直接使用 [] 。

        if valid_login(username, password):
            print '验证成功'
            return log_the_user_in(username)
        else:
            print '验证不成功'
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    # return render_template('login.html', error=error)
    return error


def valid_login(username, password):
    if username == 'lrw' and password == '123456':
        return True
    else:
        return False


def log_the_user_in(username):
    username = username.encode('utf8') if isinstance(username, unicode) else username
    return '恭喜 %s 成功登陆' % username


# ----------------------------------------------------------------------------


@app.route('/redirect_to_index')
def redirect_to_index():
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    abort(401)
    this_is_never_executed()


def this_is_never_executed():
    return 'this_is_never_executed'


@app.errorhandler(401)  # 注册了page_not_found函数专门用来处理401错误，上述 abort(401) 引发401的错误后，该函数就会被调用
def page_not_found(error):
    print type(error), error
    return 'This page does not exist', 401
    # return render_template('page_not_found.html'), 404


@app.route('/make_404')
def make_404():
    abort(404)


@app.errorhandler(404)
def not_found(error):
    # resp = make_response(render_template('error.html'), 404)  # 如果想要在视图内掌控响应对象的结果,可以使用 make_response() 函数
    resp = make_response('page does not exist', 404)
    resp.headers['X-Something'] = 'A value'
    print type(resp), resp
    print dir(resp)
    print resp.headers
    return resp


# ---------------------   使用会话、登录登出 ---------------------------

# 会话对象 相当于用密钥签名加密的 cookie，即用户可以查看你的 cookie ，但是如果没有密钥就无法修改它。
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/index_3')
def index_3():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])  # escape() 是用来转义的
    return 'You are not logged in'
    # return redirect(url_for('login_3'))


@app.route('/index_3/login_3', methods=['GET', 'POST'])
def login_3():
    if request.method == 'POST':
        session['username'] = request.form['username']  # 尚未了解表单提交
        # session['username'] = request.args.get('username', '')
        return redirect(url_for('index_3'))
    return '''
        <form method="post">
            <p><input type=text name=username>name</p>
            <p><input type=text age=userage>age</p>
            <p><input type=submit value=Login>
        </form>
    '''
    # 填完表单后会用post再次请求这个接口; name=username , 填入的表单数据存放在会话中。


@app.route('/index_3/logout_3')
def logout_3():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index_3'))


# ----------------------------------------------------------------------------


@app.route('/index_4')
def index_4():
    return render_template('index.html')


@app.route('/index_4/login', methods=['GET', 'POST'])
def login_4():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
           request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index_4'))
    return render_template('login.html', error=error)


app.logger.debug('这是个测试: A value for debugging')
app.logger.warning('这是个测试: A warning occurred (%d apples)', 42)
app.logger.error('这是个测试: An error occurred')
