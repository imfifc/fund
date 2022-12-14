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
