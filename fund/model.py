
from sqlalchemy import Column, Integer, String, DateTime, Float
from flask_sqlalchemy import SQLAlchemy

from fund.server import app

# db = SQLAlchemy(app)
#
#
# class FundRand(db.Model):
#     __tablename__ = 'fund'
#     id = Column('fund_id', Integer, primary_key=True)
#     name = Column(String(100))
#     code = Column(String(50))
#     last3month = Column(Float)
#
#     def __init__(self, name, code, last3month):
#         self.name = name
#         self.code = code
#         self.last3month = last3month
#
#     def __repr__(self):
#         return '<User %r>' % self.name
