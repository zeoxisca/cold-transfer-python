import route
import time
import re
import random
from models import User, db, Admin, Order, Deliver, Message, Alert, Car, Man, Info, Product
from flask import render_template, session, redirect, url_for

import hashlib


ALERT_MSG = ['testmsg-level1','testmsg-level2','testmsg-level3','testmsg-level4']
ALERT_TITLE = ['testtesttitle-level1','testtesttitle-level2','testtesttitle-level3','testtitle-level4']

def show_page():
    data = {}
    man = Man.query.all()

    data['man'] = man

    data['user'] = User.query.all()

    data['admin'] = Admin.query.all()

    data['product'] = Product.query.all()

    data['order'] = Order.query.filter_by().all()

    data['info'] = Info.query.all()

    data['car'] = Car.query.filter_by(active=0).all()

    return render_template('superadd.html', data=data)


def add_car(form):
    place = form['place']
    active = form['active']
    mid = form['man']
    cplace = form['cnum'][:2]
    cnumber = form['cnum'][2:]

    car = Car.query.filter_by(cplace=cplace, cnumber=cnumber).first()
    if not car:
        new_car = Car(
            cid=str(time.time())[:9]+str(random.randint(10, 99)),
            mid=mid,
            status=place,
            active=active,
            cplace=cplace,
            cnumber=cnumber
        )
        db.session.add(new_car)
    else:
        car.status = place
        car.active = active
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
    if order.status == 2:
        return redirect(url_for("superadd_page"))
    addr = order.addr
    cid = form['cid']

    car = Car.query.filter_by(cid=cid).first()

    mid = car.mid

    car.active = 1

    status = form['status']
    car.status = form['status']

    did = str(time.time())[:9] + str(random.randint(10, 99))
    new_deliver = Deliver(
        did=did,
        oid=oid,
        status=status,
        addr=addr,
        mid=mid,
        cid=cid
    )

    order.did = did
    if not order.status:
        order.status = 1
        iid = str(time.time())[:9] + str(random.randint(10, 99))
        new_info = Info(
            iid=iid,
            oid=oid,
            toxic=28,
            med=90,
            water=80,
            temp=0,
            moist=88,
            store=0,
        )
        order.iid = iid
        db.session.add(new_info)

    db.session.add(new_deliver)
    db.session.commit()

    return redirect(url_for("superadd_page"))


def add_info(form):
    item = 0
    oid = form['oid']

    iid = str(time.time())[:9] + str(random.randint(10, 99))

    score = 0

    if float(form['toxic']) > 30:
        score += 1
        item += pow(2, 5)
    elif float(form['toxic']) > 28:
        score += 0.1
        item += pow(2, 5)
    elif float(form['toxic']) > 25:
        score += 0.01
        item += pow(2, 5)

    if float(form['med']) < 90:
        score += 1
        item += pow(2, 4)
    elif float(form['med']) < 93:
        score += 0.1
        item += pow(2, 4)
    elif float(form['med']) < 95:
        score += 0.01
        item += pow(2, 4)

    if float(form['water']) < 73:
        score += 1
        item += pow(2, 3)
    elif float(form['water']) < 75:
        score += 0.1
        item += pow(2, 3)
    elif float(form['water']) < 80:
        score += 0.01
        item += pow(2, 3)

    if float(form['temp']) > 4 or float(form['temp']) < -0.5:
        score += 1
        item += pow(2, 2)
    elif float(form['temp']) > 3.5 or float(form['temp']) < 0:
        score += 0.1
        item += pow(2, 2)
    elif float(form['temp']) != 1:
        score += 0.01
        item += pow(2, 2)

    if float(form['moist']) > 95 or float(form['moist']) < 85:
        score += 1
        item += pow(2, 1)
    elif float(form['moist']) > 93 or float(form['moist']) < 87:
        score += 0.1
        item += pow(2, 1)
    elif float(form['moist']) != 90:
        score += 0.01
        item += pow(2, 1)

    if int(form['store']) > 14:
        score += 1
        item += pow(2, 0)
    elif int(form['store']) > 10:
        score += 0.1
        item += pow(2, 0)
    elif int(form['store']) > 7:
        score += 0.01
        item += pow(2, 0)

    level = 0
    if score > 2:
        level = 4
    elif score > 0.2:
        level = 3
    elif score > 0.02:
        level = 2
    else:
        level = 1

    new_info = Info(
        toxic=form['toxic'],
        med=form['med'],
        water=form['water'],
        moist=form['moist'],
        store=form['store'],
        temp=form['temp'],
        iid=iid,
        level=level,
        oid=oid,
    )

    order = Order.query.filter_by(oid=oid).first()
    order.iid = iid

    db.session.add(new_info)
    db.session.commit()

    if level != 0:
        aids = db.session.query(Admin.aid).all()
        for i in aids:
            new_alert = Alert(
                msgfor=2,
                toid=str(i[0]),
                msg=ALERT_MSG[level-1],
                title=ALERT_TITLE[level-1],
                oid=oid,
                item=item,
                valid=1,
                level=level-1,
                iid=iid,
            )
            order.alevel = level-1
            db.session.add(new_alert)
            db.session.commit()

    return redirect(url_for("superadd_page"))


