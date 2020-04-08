import app
from flask import render_template, request, session, redirect, url_for
from urllib import parse
import users, orders, testin, alerts, cars

url = app.app


@url.route('/')
def hello_world():
    return render_template('hello.html', Title='test')


@url.route('/home')
def hello1():
    return render_template('hello.html', Title='test')


@url.route('/good')
def hello():
    return 0


@url.route('/user/login/')
def show_login():
    if session.get('uid'):
        return redirect(url_for('error', msg='已登录', info='似乎你已经登陆了，去首页看看吧', link="user"))
    return users.show()


@url.route('/user/verify', methods=['POST'])
def login():
    if session.get('uid'):
        return redirect(url_for('error', msg='已登录', info='似乎你已经登陆了，去首页看看吧', link="user"))
    data = request.form
    return users.login(data)


@url.route('/user/logout/')
def logout():
    return users.logout()


@url.route('/user/register', methods=['POST','GET'])
def s_register():
    if session.get('uid'):
        return redirect(url_for('error', msg='已登录', info='似乎你已经登陆了，去首页看看吧', link="user"))
    return render_template('register.html')


@url.route('/user/rverify', methods=['POST'])
def register():
    return users.register(request.form)


@url.route('/admin/login', methods=['GET'])
def show_admin_login():
    return render_template('alogin.html')


@url.route('/admin/verify/', methods=['POST'])
def admin_login():
    if session.get('aid'):
        return redirect(url_for('backstage'))
    data = request.form
    return users.admin_login(data)


@url.route('/admin/logout/')
def admin_logout():
    return users.admin_logout()


@url.route('/error/<msg>/<info>/<link>')
def error(msg, info, link):
    data = {}
    data['msg'] = parse.unquote(msg)
    data['info'] = parse.unquote(info)
    data['link'] = '/'+parse.unquote(link)
    return render_template('error.html', data=data)


@url.route('/user/', methods=['GET'])
def userpage():
    a = session.get('uid')
    if a:
        return users.showUser(a)
    else:
        return redirect(url_for('error', msg='未登录', info='未登录是不可以进来的', link='user%2flogin'))


@url.route('/user/update')
def updatepage():
    a = session.get('uid')
    if a:
        return users.updatepage()
    else:
        return redirect(url_for('error', msg='未登录', info='未登录是不可以进来的', link='user%2flogin'))


@url.route('/user/update/post', methods=['POST'])
def userupdate():
    return users.update(request.form)


@url.route('/user/orders/')
def userorder():
    a = session.get('uid')
    if a:
        return orders.show_user_orders()
    else:
        return redirect(url_for('error', msg='未登录', info='未登录是不可以进来的', link='user%2flogin'))


@url.route('/admin/backstage')
def backstage():
    if not session.get('aid'):
        return redirect(url_for('error', msg='未登录', info='未登录是不可以进来的', link='admin%2flogin'))
    else:
        return users.show_backstage()


@url.route('/testpage')
def testpage():
    return render_template('superadd.html')


@url.route('/superadd')
def superadd_page():
    return testin.show_page()


@url.route('/superadd/man', methods=['POST'])
def addman():
    return testin.add_man(request.form)


@url.route('/superadd/car', methods=['POST'])
def addcar():
    return testin.add_car(request.form)


@url.route('/superadd/admin', methods=['POST'])
def addadmin():
    return testin.add_admin(request.form)


@url.route('/superadd/product', methods=['POST'])
def addproduct():
    return testin.add_product(request.form)


@url.route('/superadd/order', methods=['POST'])
def addorder():
    return testin.add_order(request.form)


@url.route('/superadd/deliver', methods=['POST'])
def adddeliver():
    return testin.add_deliver(request.form)


@url.route('/superadd/info', methods=['POST'])
def addinfo():
    return testin.add_info(request.form)


@url.route('/order/<oid>')
def order_page(oid):
    return orders.order_page(oid)


@url.route('/searchorder', methods=['GET'])
def search_order():
    return redirect(url_for('order_page', oid=request.args.get('oid')))


@url.route('/admin/orders/')
def admin_orders():
    return orders.show_orders()


@url.route('/admin/alerts')
def admin_alerts():
    return alerts.show_alerts()


@url.route('/admin/delivers/')
def admin_delivers():
    return orders.admin_delivers()


@url.route('/admin/users')
def admin_users():
    return users.admin_users()


@url.route('/admin/cars')
def admin_cars():
    return cars.admin_cars()


@url.route('/admin/delalert/<id>')
def del_alert(id):
    return alerts.del_alerts(id)


@url.route('/alert/read/<id>')
def read_alert(id):
    return alerts.read_alert(id)

