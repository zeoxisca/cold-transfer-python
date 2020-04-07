from models import Order, db, User, Admin, Deliver, Product, Man, Car, Info, Alert
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


def get_admin_name(aid):
    admin = Admin.query.filter_by(aid=aid).first()
    return admin.a_name


def get_user_name(uid):
    user = User.query.filter_by(uid=uid).first()
    return user.user_name


def order_page(oid):
    if not session.get('uid') and not session.get('aid'):
        return redirect(url_for('error', msg='请先登录', info='未登录不可查询订单', link='home'))
    order = Order.query.filter_by(oid=oid).first()

    if not order:
        if session.get('uid'):
            return redirect(url_for('error', msg='查无此单', info='请仔细检查订单号码', link='user'))
        if session.get('aid'):
            return redirect(url_for('error', msg='查无此单', info='请仔细检查订单号码', link='admin%2fbackstage'))

    user = User.query.filter_by(uid=order.uid).first()
    admin = Admin.query.filter_by(aid=order.aid).first()

    if session.get('uid') != order.uid and not session.get('aid'):
        return redirect(url_for('error', msg='请求错误', info='只能查询和自己相关的订单', link='home'))

    name = ''

    if session.get('uid'):
        name = get_user_name(session.get('uid'))
    else:
        name = get_admin_name(session.get('aid'))

    product = Product.query.filter_by(pid=order.pid).first()

    delivers = None
    info = None

    if order.status == 0:
        pass
    else:
        delivers = db.session.query(
            Deliver.did,
            Deliver.status,
            Car.cplace,
            Car.cnumber,
            Man.name,
            Man.tel,
            Deliver.created_at
        ).filter(
            Deliver.oid == order.oid,
            Deliver.cid == Car.cid,
            Car.mid == Man.mid
        ).order_by(
            Deliver.updated_at.desc()
        ).all()

        info = Info.query.filter_by(oid=oid).order_by(Info.created_at.desc()).all()


    data = {}
    data['user'] = {'name': name}

    data['order'] = {
        'oid': oid,
        'product': product.pname,
        'pid': product.pid,
        'price': (product.price * order.sum) / 100,
        'sum': order.sum,
        'o_price': product.price,
        'created_at': order.created_at,
        'addr': order.addr,
        'tel': user.tel,
        'status': order.status,
        'updated_at': order.updated_at,
    }

    if order.status:
        data['delivers'] = list(delivers)
        data['info'] = info
        data['len1'] = len(list(delivers))
        data['len2'] = len(list(info))
    else:
        data['delivers'] = None
        data['info'] = None
        data['len1'] = 0
        data['len2'] = 0

    return render_template('order.html', data=data)


def show_orders():
    aid = session.get('aid')
    if not aid:
        return redirect(url_for('error', msg='请登录', info='这是管理员才能查看的页面', link='admin%2flogin'))

    send_orders = db.session.query(
        Order.oid,
        Product.pname,
        Order.sum,
        Product.price,
        User.user_name,
        User.tel,
        Order.addr,
        Order.status,
        Info,
        Deliver,
        Car,
        Man
    ).filter(
        Order.did == Deliver.did,
        Order.iid == Info.iid,
        User.uid == Order.uid,
        Car.cid == Deliver.cid,
        Man.mid == Car.mid,
        Order.pid == Product.pid
    ).order_by(Order.created_at.desc()).all()

    unsend_orders = db.session.query(
        Order.oid,
        Product.pname,
        Order.sum,
        Product.price,
        User.user_name,
        User.tel,
        Order.addr
    ).filter(
        User.uid == Order.uid,
        Order.status == 0,
        Product.pid == Order.pid
    ).order_by(Order.created_at.desc()).all()

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

    data = {}
    data['name'] = Admin.query.filter_by(aid=aid).first().a_name
    data['send'] = send_orders
    data['unsend'] = unsend_orders
    data['alert_num'] = Alert.query.filter_by(msgfor=2, toid=aid, valid=1).count()
    data['level'] = level

    data['send_len'] = len(send_orders)
    data['send_row_len'] = data['send_len'] // 3
    if data['send_len'] % 3 != 0:
        data['send_row_len'] += 1
    data['unsend_len'] = len(unsend_orders)
    data['unsend_row_len'] = data['unsend_len'] // 3
    if data['unsend_len'] % 3 != 0:
        data['unsend_row_len'] += 1
    data['all_len'] = len(send_orders) + len(unsend_orders)
    data['all_row_len'] = data['send_row_len'] + data['unsend_row_len']


    lenlen = 0
    for i in send_orders:
        if i[7] == 2:
            lenlen += 1

    data['end_len'] = lenlen
    data['end_row_len'] = data['end_len'] // 3
    if data['end_len'] % 3 != 0:
        data['end_row_len'] += 1

    return render_template('orders.html', data=data)