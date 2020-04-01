from models import Order, db
from flask import render_template, session, redirect, url_for
import random, time


def show_user_orders():
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('error', msg='未登录', info='不登录怎么知道你有什么订单呢', link='user%2flogin'))

    orders = Order.query.filter_by(uid=uid).all()

    return render_template('test.html', data=orders)


def show_a_orders():
    aid = session.get('aid')
    if not aid:
        return redirect(url_for('error', msg='未登录', info='不登录怎么知道你有什么订单呢', link='admin%2flogin'))

    orders = Order.query.filter_by(aid=aid).all()

    return render_template('test.html', data=orders)


def add_orders_only(order):
    oid = str(time.time())[:8] + str(random.randint(10, 99))
    uid = order['uid']
    aid = order['aid']
    sum = order['count']
    pid = order['pid']

    did = str(time.time())[:8] + str(random.randint(10, 99))




    pass

