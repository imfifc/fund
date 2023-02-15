import os
from pathlib import Path

from flask import Flask, request, flash, url_for, redirect, render_template, jsonify, Response, make_response, \
    send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from gevent import pywsgi
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from flask_migrate import Migrate

from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from werkzeug.utils import secure_filename
from pyecharts.faker import Faker

# from fund.model import FundRand, db

# app = Flask(__name__, static_folder="static")  # static file 切记不要写错哦
import pymysql

# from fund import user
from fund import user
from fund.data import aggreate_data
from fund.models import FundRand, DayGrowRate, Last1month, Last6month, Last1week, Last1year
from fund.dbs import db


def create_app():
    app = Flask(__name__)  # static file 切记不要写错哦
    app.register_blueprint(user.bp)

    app.config['JSON_AS_ASCII'] = False
    # 这里连接串的意思是使用pymysql去连接mysql
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3316/mytest'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fund3.sqlite3'
    app.config['SECRET_KEY'] = "random string"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    CORS(app, supports_credentials=True)
    # init_app就是为了解决循环引用的
    db.init_app(app)
    manager = Manager(app)
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)
    # 第一个参数是flask的实现，第二个参数是sqlalchemy数据库实例
    # migrate = Migrate(app, db)
    # manager是flask-scriptde 实例，这条语句在flask-script中添加一个db命令
    # manager.add_command('db', MigrateCommand)

    # pymysql.install_as_MySQLdb() // mysql 使用
    # db = SQLAlchemy(app)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379'
    )
    from fund.models import FundRand

    # with app.app_context():
    #     db.create_all()

    return app
