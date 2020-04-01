import route
import time
import re
import random
from models import User, db, Admin, Order, Deliver, Message, Alert, Car, Man, Info, Product
from flask import render_template, session, redirect, url_for

import hashlib


def show_page():
    data = {}
    man = Man.query.all()

    data['man'] = man

    data['user'] = User.query.all()

    data['admin'] = Admin.query.all()

    data['product'] = Product.query.all()

    data['order'] = Order.query.filter_by(did=None).all()

    data['info'] = Info.query.all()

    data['car'] = Car.query.filter_by(active=0).all()

    return render_template('superadd.html', data=data)


def add_car(form):
    place = form['place']
    active = form['active']
    mid = form['man']
    cplace = form['cnum'][:2]
    cnumber = form['cnum'][2:]

    new_car = Car(
        cid = str(time.time())[:9]+str(random.randint(10, 99)),
        mid=mid,
        status=place,
        active=active,
        cplace=cplace,
        cnumber=cnumber
    )
    db.session.add(new_car)
    db.session.commit()
    return redirect(url_for('superadd_page'))


def add_man(form):
    name = form['name']
    tel = form['tel']
    mid = str(time.time())[:9]+str(random.randint(10, 99))
    new_user = Man(
        mid=mid,
        name=name,
        tel=tel,
        )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('superadd_page'))


def add_order(form):
    oid = str(time.time())[:9]+str(random.randint(10, 99))
    uid = form['uid']
    aid = form['aid']
    sum = form['num']
    pid = form['pid']
    addr = form['aim']

    new_order = Order(
        oid=oid,
        uid=uid,
        aid=aid,
        sum=sum,
        pid=pid,
        addr=addr
    )
    db.session.add(new_order)
    db.session.commit()

    return redirect(url_for('superadd_page'))


def add_admin(form):
    username = form['username']
    pwd = form['pwd']

    new_admin = Admin(
        aid=str(time.time())[:9]+str(random.randint(10, 99)),
        a_name=username,
        pwd=hashlib.md5(pwd.encode('utf-8')).hexdigest()
    )
    db.session.add(new_admin)
    db.session.commit()

    return redirect(url_for('superadd_page'))


def add_product(form):
    pname = form['pname']
    price = form['price']
    price = int(float(price)*100)
    pid = str(time.time())[:9]+str(random.randint(10, 99))

    new_p = Product(
        pid=pid,
        price=price,
        pname=pname
    )

    db.session.add(new_p)
    db.session.commit()
    return redirect(url_for('superadd_page'))


def add_msgs(form):
    pass


def add_alert(form):
    pass


def add_deliver(form):
    oid = form['oid']
    order = Order.query.filter_by(oid=oid).first()

    addr = order.addr
    cid = form['cid']

    mid = Car.query.filter_by(cid=cid).first().mid

    status = form['status']

    if order.did == 0:
        iid = str(time.time())[:9] + str(random.randint(10, 99)),
        new_info = Info(
            iid=iid,
            toxic=28,
            med=90,
            water=80,
            temp=0,
            moist=88,
            store=0,
        )
        did = str(time.time())[:9] + str(random.randint(10, 99))
        new_deliver = Deliver(
            did=did,
            iid=iid,
            status=status,
            addr=addr,
            mid=mid,
            cid=cid
        )

        order.did = did
        order.status = 1

        db.session.add(new_info)
        db.session.add(new_deliver)
        db.session.commit()
    elif order.did == 1:
        deliver = Deliver.query.filter_by(did=order.did).first()
        deliver.status = status

        db.session.commit()
    else:
        pass

    return redirect(url_for("superadd_page"))


def add_info(form):
    iid = form['iid']

    info = Info.query.filter_by(iid=iid).first()

    info.toxic = form['toxic']
    info.med = form['med']
    info.water = form['water']
    info.moist = form['moist']
    info.store = form['store']
    info.temp = form['temp']

    db.session.commit()

    # sendmsg

    return redirect(url_for("superadd_page"))


