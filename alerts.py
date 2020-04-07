from models import Order, db, User, Admin, Deliver, Product, Man, Car, Info, Alert
from flask import render_template, session, redirect, url_for
import random, time


def show_alerts():
    aid = session.get('aid')

    if not aid:
        return redirect(url_for('error', msg='未登录', info='需要先登录', link='admin%2flogin'))

    alerts = db.session.query(
        Alert,
        Info,
        Product.pname
    ).filter(
        Alert.msgfor == 2,
        Alert.toid == aid,
        Alert.oid == Order.oid,
        Order.pid == Product.pid,
        Info.iid == Alert.iid
    ).order_by(Alert.created_at).all()

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
    data['alerts'] = alerts
    data['name'] = Admin.query.filter_by(aid=aid).first().a_name
    data['alert_num'] = Alert.query.filter_by(msgfor=2, toid=aid, valid=1).count()
    data['alert_len'] = len(alerts)
    level = 0
    for i in alerts:
        if i[0].level > level:
            level = i[0].level

    data['level'] = level+1
    return render_template('alerts.html', data=data)


def del_alerts(id):
    alert = Alert.query.filter_by(id=id).first()
    db.session.delete(alert)

    db.session.commit()

    return redirect(url_for('admin_alerts'))