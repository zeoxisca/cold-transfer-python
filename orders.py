from models import Order, db, User, Admin, Deliver, Product, Man, Car, Info
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

    if session.get('uid') != order.uid and session.get('aid') != order.aid:
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