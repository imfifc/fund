from werkzeug.security import generate_password_hash

from fund.dbs import db


class FundRand(db.Model):
    __tablename__ = 'fund'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    type = db.Column(db.String(10))
    name = db.Column(db.String(100))
    last3month = db.Column(db.Float)
    date = db.Column(db.String(30), default=None)

    # create_date = db.Column(db.DateTime, default=datetime.now, index=True)
    # update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

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