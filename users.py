import route
import time
import re
import random
from models import User, db, Admin, Order, Deliver, Message, Alert, Product, Car
from flask import render_template, session, redirect, url_for

import hashlib


def show():
    return render_template('login.html')


def login(data):

    username = data['username']
    pwd = data['pwd']

    user = User.query.filter_by(user_name=username).first()

    if not user:
        msg = '未注册'
        info = '系统中没有你的信息，点击下一步注册'
        link = '/user%2fregister'
        return redirect(url_for('error', msg=msg, info=info, link=link))

    if hashlib.md5(pwd.encode('utf-8')).hexdigest() == user.pwd:
        session['uid'] = user.uid
        return redirect(url_for('userpage'))
    else:
        return redirect(url_for('error', msg='密码错误', info='你的信息填写有点问题', link='user%2flogin'))


def logout():
    if session.get('uid') is None:
        return redirect(url_for('error', msg='未登录', info='城外的人还没进去，就想出来？', link='user%2flogin'))
    else:
        session.pop('uid')
        return redirect(url_for('error', msg='成功登出', info='下次来玩呀', link='home'))


def register(data):
    username = data['username']
    tel = data['tel']
    pwd = data['pwd']
    c_pwd = data['confirmpwd']

    ifuser = User.query.filter_by(user_name=username).first()
    iftel = User.query.filter_by(tel=tel).first()

    if ifuser:
        return redirect(url_for('error', msg='用户名已注册', info='用户名已存在，请登录', link='user%2flogin'))
    if iftel:
        return redirect(url_for('error', msg='手机已注册', info='手机号已存在，请登录', link='user%2flogin'))

    if c_pwd != pwd:
        return redirect(url_for('error', msg='确认密码错误', info='两次输入的密码不一致，请核对', link='user%2fregister'))

    ret = re.match(r"^1[35678]\d{9}$", tel)
    if not ret:
        return redirect(url_for('error', msg='格式错误！', info='手机号格式错误，请重新输入', link='user%2fregister'))

    new_user = User(
        uid=str(time.time())[:6]+str(random.randint(10, 99)),
        user_name=username,
        tel=tel,
        pwd=str(hashlib.md5(pwd.encode('utf-8')).hexdigest()),
        )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('error', msg='注册成功', info='已经注册成功了，去登陆', link='user%2flogin'))


def showUser(uid):

    if uid != session.get('uid'):
        session.pop('uid')
        return redirect(url_for('error', msg='身份信息有误', info='你好像不是你，请尝试重新登录', link='user%2flogin'))

    user = User.query.filter_by(uid=uid).first()
    if user:
        user_data = {}
        user_data['name'] = user.user_name
        user_data['uid'] = uid
        user_data['tel'] = user.tel
        user_data['addr'] = user.addr

        orders = Order.query.filter_by(uid=uid).all()

        unrecieved = db.session.query(Order.oid, Product.pname, Deliver.updated_at, Deliver.status). \
            filter(Order.status == 1).\
            filter(Product.pid == Order.pid, Deliver.did == Order.did, Order.uid == uid)
            # join(Order, Product.pid == Order.pid, Deliver.did == Order.did).\

        unsended = db.session.query(Order.oid, Product.pname, Order.created_at, Order.addr). \
            filter(Order.status == 0).\
            filter(Product.pid == Order.pid, Order.uid == uid)

        received = db.session.query(Order.oid, Product.pname, Deliver.updated_at, Order.addr). \
            filter(Order.status == 2).\
            filter(Product.pid == Order.pid, Deliver.did == Order.did, Order.uid == uid)

        orders = db.session.query(Order.oid, Product.pname, Order.updated_at, Order.status). \
            filter(Product.pid == Order.pid, Order.uid == uid)

        data = {}
        data['user'] = user_data
        data['unsended'] = unsended
        data['received'] = received
        data['unreceived'] = unrecieved
        data['orders'] = orders

        return render_template('userpage.html', data=data)
    else:
        session.pop('uid')
        return redirect(url_for('error', msg='身份信息有误', info='你好像不是你，请尝试重新登录', link='user%2flogin'))


def admin_login(form):
    username = form['username']
    pwd = form['pwd']

    admin = Admin.query.filter_by(a_name=username, pwd=str(hashlib.md5(pwd.encode('utf-8')).hexdigest())).first()

    if not admin:
        return redirect(url_for('error', msg='身份信息有误', info='用户名或密码错误，请重新输入', link='admin%2flogin'))

    else:
        session['aid'] = admin.aid
        return redirect(url_for('backstage'))


def admin_logout():
    if not session.get('aid'):
        return redirect(url_for('error', msg='未登录', info='没登陆过干嘛登出', link='admin%2flogin'))
    else:
        session.pop('aid')
        return redirect(url_for('hello_world'))


def show_backstage():
    if not session.get('aid'):
        return redirect(url_for('error', msg='身份信息有误', info='身份信息已过期，请重新登录', link='admin%2flogin'))
    admin = Admin.query.filter_by(aid=session.get('aid')).first()
    if not admin:
        return redirect(url_for('error', msg='身份信息有误', info='查无此人，请合理使用系统', link='admin%2flogin'))

    aname = admin.a_name
    aid = session.get('aid')
    orders = Order.query.filter(Order.status == 1).all()
    order = []
    order_num = Order.query.count()
    d_num = Car.query.filter(Car.active == 1).count()
    n_num = Order.query.filter(Order.status != 2).count()
    mem_num = User.query.count()
    msg_num = Message.query.filter_by(msgfor=2).count()
    a_num = Alert.query.filter_by(msgfor=2, toid=aid, valid=1).count()

    if Alert.query.filter_by(toid=aid, msgfor=2, level=3, valid=1).count() > 0:          # 顶级
        level = 4
    elif Alert.query.filter_by(toid=aid, msgfor=2, level=2, valid=1).count() > 0:
        level = 3
    elif Alert.query.filter_by(toid=aid, msgfor=2, level=1, valid=1).count() > 0:        # 开始弹窗
        level = 2
    elif Alert.query.filter_by(toid=aid, msgfor=2, level=0, valid=1).count() > 0:
        level = 1
    else:                                                           # 无事
        level = 0

    for i in orders:
        temp = {}
        temp['oid'] = i.oid
        temp['addr'] = i.addr
        temp['time'] = i.updated_at
        deliver = Deliver.query.filter_by(did=i.did).first()
        if deliver:

            temp['now'] = deliver.status

        order.append(temp)

    data = {
        'aname': aname,
        'orders': order,
        'num1': order_num,
        'num2': d_num,
        'num3': n_num,
        'num4': mem_num,
        'level': level,
        'm_num': msg_num,
        'a_num': a_num,
    }

    return render_template('backstage.html', data=data)


def updatepage():
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('error', msg='未登录', info='未登录不可进入', link='user%2flogin'))

    user = User.query.filter_by(uid=uid).first()

    return render_template('userupdate.html', data=user)


def update(form):
    tel = form['tel']
    username = form['username']
    addr = form['addr']

    uid = session.get('uid')

    user = User.query.filter_by(uid=uid).first()

    user.tel = tel
    user.user_name = username
    user.addr = addr

    db.session.commit()

    return redirect(url_for('userpage'))