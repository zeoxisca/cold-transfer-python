from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(20), unique=True, nullable=False)
    user_name = db.Column(db.String(40), unique=True)
    pwd = db.Column(db.String(120), nullable=False)
    tel = db.Column(db.String(11), nullable=False)
    addr = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.user_name


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.String(20), unique=True, nullable=False)
    pwd = db.Column(db.String(120), nullable=False)
    a_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.a_name


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    oid = db.Column(db.String(20), unique=True, nullable=False)         # 订单id
    iid = db.Column(db.String(20), nullable=True)
    uid = db.Column(db.String(20), nullable=False)                      # 用户id
    aid = db.Column(db.String(20), nullable=False)                      # 商家id
    sum = db.Column(db.Integer, nullable=False)                         # 数量
    pid = db.Column(db.String(20), nullable=False)                      # 商品id
    did = db.Column(db.String(20), nullable=True)                       # 最新的运输id
    status = db.Column(db.Integer, default=0)                           # 0:未发货, 1:未收货, 2:已完成
    addr = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'),
                           server_onupdate=db.text('CURRENT_TIMESTAMP'), nullable=False)


class Deliver(db.Model):
    __tablename__ = 'delivers'
    id = db.Column(db.Integer, primary_key=True)
    did = db.Column(db.String(20), nullable=False, unique=True)
    oid = db.Column(db.String(20), nullable=False)
    cid = db.Column(db.String(20), nullable=False)  # 车id
    mid = db.Column(db.String(20), nullable=False)  # 驾驶员id
    addr = db.Column(db.Text, nullable=False)       # 目的地
    status = db.Column(db.Text, nullable=False)     # 目前位置

    created_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'),
                           server_onupdate=db.text('CURRENT_TIMESTAMP'), nullable=False)


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.String(20), unique=True, nullable=False)
    mid = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Text, nullable=False)         # 目前位置
    active = db.Column(db.Integer)                      # 是否活跃
    cplace = db.Column(db.String(4), nullable=False)
    cnumber = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'),
                           server_onupdate=db.text('CURRENT_TIMESTAMP'), nullable=False)


class Man(db.Model):
    __tablename__ = 'men'
    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    tel = db.Column(db.String(13), nullable=False)


class Info(db.Model):
    __tablename__ = 'infos'
    id = db.Column(db.Integer, primary_key=True)
    iid = db.Column(db.String(20), unique=True, nullable=False)
    oid = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)    # 0: 无所谓， 1: 接近范围， 2: 1-2项超过， 3:3项以上超过
    toxic = db.Column(db.Float)
    med = db.Column(db.Float)
    water = db.Column(db.Float)
    temp = db.Column(db.Float)
    moist = db.Column(db.Float)
    store = db.Column(db.Integer)

    created_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'),nullable=False)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    msgfor = db.Column(db.Integer, nullable=False, default=0)    # 1: 给用户 2: 给商家
    toid = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)

    valid = db.Column(db.Integer, nullable=False, default=1)  # 0: 读过，1: 未读。

    created_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'),nullable=False)


class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    msgfor = db.Column(db.Integer, nullable=False, default=0)  # 0: 广播， 1: 给用户 2: 给商家
    toid = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)    # 0: 轻微偏离， 1: 接近范围， 2: 1-2项超过， 3:3项以上超过
    oid = db.Column(db.String(20), nullable=False)
    item = db.Column(db.Integer, nullable=False)            # max: 63 111111

    valid = db.Column(db.Integer, nullable=False, default=1)    # 0: 读过，1: 未读。

    created_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'), nullable=False)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.String(20), nullable=False)
    pname = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
