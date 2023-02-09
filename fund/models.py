import datetime

from werkzeug.security import generate_password_hash

from fund.dbs import db


class FundRand(db.Model):
    __tablename__ = 'fund'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10))
    type = db.Column(db.String(10))
    name = db.Column(db.String(100))
    last3month = db.Column(db.Float)
    date = db.Column(db.String(30), default=None)

    create_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, index=True)
    update_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # 是否被删除
    is_delete = db.Column(db.BOOLEAN, default=False)

    # create_date = db.Column(db.DateTime, default=datetime.now, index=True)
    # update_time = db.Column(db.DateTime(6), default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, code, last3month, date, type):
        self.name = name
        self.code = code
        self.last3month = last3month
        self.date = date
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.name

    def tojson(self):
        return {
            'id': self.id,
            'code': self.code,
            'type': self.type,
            'name': self.name,
            'last3month': self.last3month,
            'date': self.date,
        }


class DayGrowRate(db.Model):
    __tablename__ = 'dayGrowRate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10))
    type = db.Column(db.String(10))
    name = db.Column(db.String(100))
    dayGrowRate = db.Column(db.Float)
    date = db.Column(db.String(30), default=None)

    create_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, index=True)
    update_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # 是否被删除
    is_delete = db.Column(db.BOOLEAN, default=False)

    # create_date = db.Column(db.DateTime, default=datetime.now, index=True)
    # update_time = db.Column(db.DateTime(6), default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, code, dayGrowRate, date, type):
        self.name = name
        self.code = code
        self.dayGrowRate = dayGrowRate
        self.date = date
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.name

    def tojson(self):
        return {
            'id': self.id,
            'code': self.code,
            'type': self.type,
            'name': self.name,
            'dayGrowRate': self.dayGrowRate,
            'date': self.date,
        }


class Last1week(db.Model):
    __tablename__ = 'last1week'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10))
    type = db.Column(db.String(10))
    name = db.Column(db.String(100))
    last1week = db.Column(db.Float)
    date = db.Column(db.String(30), default=None)

    create_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, index=True)
    update_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # 是否被删除
    is_delete = db.Column(db.BOOLEAN, default=False)

    # create_date = db.Column(db.DateTime, default=datetime.now, index=True)
    # update_time = db.Column(db.DateTime(6), default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, code, last1week, date, type):
        self.name = name
        self.code = code
        self.last1week = last1week
        self.date = date
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.name

    def tojson(self):
        return {
            'id': self.id,
            'code': self.code,
            'type': self.type,
            'name': self.name,
            'last1week': self.last1week,
            'date': self.date,
        }


class Last1month(db.Model):
    __tablename__ = 'last1month'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10))
    type = db.Column(db.String(10))
    name = db.Column(db.String(100))
    last1month = db.Column(db.Float)
    date = db.Column(db.String(30), default=None)

    create_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, index=True)
    update_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # 是否被删除
    is_delete = db.Column(db.BOOLEAN, default=False)

    # create_date = db.Column(db.DateTime, default=datetime.now, index=True)
    # update_time = db.Column(db.DateTime(6), default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, code, last1month, date, type):
        self.name = name
        self.code = code
        self.last1month = last1month
        self.date = date
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.name

    def tojson(self):
        return {
            'id': self.id,
            'code': self.code,
            'type': self.type,
            'name': self.name,
            'last1month': self.last1month,
            'date': self.date,
        }


class Last6month(db.Model):
    __tablename__ = 'last6month'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10))
    type = db.Column(db.String(10))
    name = db.Column(db.String(100))
    last6month = db.Column(db.Float)
    date = db.Column(db.String(30), default=None)

    create_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, index=True)
    update_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # 是否被删除
    is_delete = db.Column(db.BOOLEAN, default=False)

    # create_date = db.Column(db.DateTime, default=datetime.now, index=True)
    # update_time = db.Column(db.DateTime(6), default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, code, last6month, date, type):
        self.name = name
        self.code = code
        self.last6month = last6month
        self.date = date
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.name

    def tojson(self):
        return {
            'id': self.id,
            'code': self.code,
            'type': self.type,
            'name': self.name,
            'last6month': self.last6month,
            'date': self.date,
        }


class Last1year(db.Model):
    __tablename__ = 'last1year'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10))
    type = db.Column(db.String(10))
    name = db.Column(db.String(100))
    last1year = db.Column(db.Float)
    date = db.Column(db.String(30), default=None)

    create_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, index=True)
    update_time = db.Column(db.DATETIME(6), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # 是否被删除
    is_delete = db.Column(db.BOOLEAN, default=False)

    # create_date = db.Column(db.DateTime, default=datetime.now, index=True)
    # update_time = db.Column(db.DateTime(6), default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, code, last1year, date, type):
        self.name = name
        self.code = code
        self.last1year = last1year
        self.date = date
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.name

    def tojson(self):
        return {
            'id': self.id,
            'code': self.code,
            'type': self.type,
            'name': self.name,
            'last1year': self.last1year,
            'date': self.date,
        }


# Create your models here.
class User(db.Model):  # 创建用户信息表
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    name_cn = db.Column(db.String(30), nullable=False)

    # create_time = db.Column(db.String(30))  # 第一次创建的时间
    # email = db.Column(db.String(30))
    @classmethod
    def add_admin(cls):
        user = db.session.query(User).filter(User.username == 'admin').first()
        if user is None:
            user = User(username='admin', password=generate_password_hash('123456'), name_cn='管理员')
            db.session.add(user)
            db.session.commit()

    def __str__(self):
        return '<User：%s>' % self.username

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return f"<title {self.title}>"


"""
model 操作
FundRand.query.all()
FundRand.query.first()
FundRand.query.get(1) 主键查询
FundRand.query.filter_by(type='zs').order_by('date').all()
FundRand.query.filter(FundRand.name.startswith('创金')).all()
FundRand.query.filter(FundRand.type != 'zq' ).all() 取反查询

from sqlalchemy import and_,or_,not_
filter只能用于范围，不能用于等号一元赋值
FundRand.query.filter(or_(FundRand.name.startswith('创金'),(FundRand.name.startswith('华夏')))).all()

FundRand.query.filter(and_(FundRand.date>='2023-02-07',FundRand.type!='zq')).all()
"""
