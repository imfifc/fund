# from fund.server import app
#
# from sqlalchemy import Column, Integer, String, DateTime, Float
# from flask_sqlalchemy import SQLAlchemy
#
#
# db = SQLAlchemy(app)
#
#
# class FundRand(db.Model):
#     __tablename__ = 'fund'
#     id = db.Column('fund_id', db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     code = db.Column(db.String(50))
#     last3month = db.Column(db.Float)
#
#     def __init__(self, name, code, last3month):
#         self.name = name
#         self.code = code
#         self.last3month = last3month
#
#     def __repr__(self):
#         return '<User %r>' % self.name
