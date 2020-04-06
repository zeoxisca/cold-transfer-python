from models import Order, db, User, Admin, Deliver, Product, Man, Car, Info, Alert
from flask import render_template, session, redirect, url_for
import random, time


def show_alerts():
    aid = session.get('aid')

    if not aid:
        return redirect(url_for('error', msg='未登录', info='需要先登录', link='admin%2flogin'))

    alerts = Alert.query.filter_by(msgfor=2, toid=aid).order_by(Alert.created_at.desc()).all()

    data = {}
    data['alerts'] = alerts
    data['name'] = Admin.query.filter_by(aid=aid).first().a_name
    data['alert_num'] = Alert.query.filter_by(msgfor=2, toid=aid, valid=1).count()

    level = 0
    for i in alerts:
        if i.level > level:
            level = i.level

    data['level'] = level+1
    return render_template('alerts.html', data=data)
