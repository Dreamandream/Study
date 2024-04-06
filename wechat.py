from flask import Flask, render_template, session, redirect, request
from flask_socketio import SocketIO, emit, send
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                       password='Study', db='wx')
cursor = conn.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
socketio = SocketIO(app)

@app.route('/regView')
def reg_view():
    return render_template('register.html')

@app.route('/reg', methods = ['POST'])
def reg():
    u = request.form.get('username')
    p = request.form.get('password')
    h = request.form.get('head')
    sql = 'select * from user where username = "%s"' % u
    cursor.execute(sql)
    r = cursor.fetchone()
    if r is not None:
        return render_template('register.html', msg = '用户名已存在')
    else:
        sql = 'insert into user values("%s", "%s", "%s")' % (u, p, h)
        cursor.execute(sql)
        conn.commit()
        return render_template('login.html')

@app.route('/loginView')
def login_view():
    return render_template('login.html')


@app.route('/index')
def chat_view():
    if session.get('user') is None:
        return render_template('login.html')
    return render_template('index.html')


# 监听用户的连接事件
@socketio.on('connect', namespace='/chat')
def user_join():
    print('连接成功')

    # 当用户的webscoket建立连接成功，给用户发送他的用户名。
    if session.get('user'):
        emit('regist', session.get('user')['username'])
        # 向所有人发送欢迎事件，使用广播模式发送消息，让所有人都能够收得到
        emit('welcome111', session.get('user')['username'], broadcast=True)

@app.route('/login', methods=['POST'])
def login():
    # 使用request从表单里获取输入框的内容
    u = request.form.get('username')
    p = request.form.get('password')
    sql = 'select * from user where username = "%s" and password = "%s"' % (u, p)
    cursor.execute(sql)
    r = cursor.fetchone()

    if r:  # 判断r是否为空，在数据库里查询是否有r数据
        user = {
            'username': r[0],
            'head': r[2]
        }
        session['user'] = user  # session用来保存用户信息
        return redirect('/index')
    return redirect('/loginView')

@socketio.on('message', namespace='/chat')
def msg(aaa):
    user = session.get('user')

    # 定义一个字典，用来保存用户名和消息内容，统一发送给所有用户
    content = {
        'from': user['username'],
        'aaa': aaa,
        'head': user['head']
    }
    # 使用广播模式把消息发给群里的所有在线用户信息
    send(content, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, port = 9090, allow_unsafe_werkzeug=True)
