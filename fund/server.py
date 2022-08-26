import json
from datetime import datetime
import time
from random import randrange

from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from pyecharts.faker import Faker

# from fund.model import FundRand, db

# app = Flask(__name__, static_folder="static")  # static file 切记不要写错哦
from fund.data import aggreate_data

app = Flask(__name__)  # static file 切记不要写错哦
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fund.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db.init_app(app)

db = SQLAlchemy(app)


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
            'code': self.code,
            'type': self.type,
            'name': self.name,
            'last3month': self.last3month,
            'date': self.date,
        }


def bar_base() -> Bar:
    # x_data = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    y_data = [820, 932, 901, 934, 1290, 1330, 1320]
    # 股票型
    x_data, gp_datas, zq_datas, zs_datas, qdii_datas, fof_datas, hh_datas = get_x_y_datas()

    c = (
        Line()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="混合型",
            # stack="总量",
            # y_axis=[320, 332, 301, 334, 390, 330, 320],
            y_axis=hh_datas,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add_yaxis(
            series_name="股票型",
            # stack="总量",
            y_axis=gp_datas,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add_yaxis(
            series_name="债券型",
            # stack="总量",
            y_axis=zq_datas,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add_yaxis(
            series_name="指数型",
            # stack="总量",
            y_axis=zs_datas,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add_yaxis(
            series_name="FOF型",
            # stack="总量",
            y_axis=fof_datas,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add_yaxis(
            series_name="QDII型",
            # stack="总量",
            y_axis=qdii_datas,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True, position="top"),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="堆叠区域图"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(boundary_gap=False, is_scale=True),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return c

    # @app.teardown_request


# def shutdown_session(exception=None):
#     db_session.remove()


@app.route('/new', methods=['GET', 'POST'])
def new():
    datas = aggreate_data()

    for data in datas:
        f = FundRand(**data)
        if not FundRand.query.filter_by(type=data.get('type'), date=data.get('date')).first():
            db.session.add(f)
        # db.session.add(f)
    db.session.commit()
    return jsonify(data=datas, code=200)


@app.route('/show')
def show():
    datas = FundRand.query.all()
    # print(res)
    datas = [i.tojson() for i in datas]
    return jsonify(data=datas, code=200)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test():
    return render_template("test.html")
    # return render_template("area-stack-gradient.html")


@app.route("/line1")
def line1():
    return render_template("line1.html")


@app.route("/line2")
def line2():
    res = ['混合型', '股票型', '债券型', '指数型', 'FOF型', 'QDII型']
    a = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    return render_template("line2.html")


@app.route("/echart")
def echart():
    x_data, gp_datas, zq_datas, zs_datas, qdii_datas, fof_datas, hh_datas = get_x_y_datas()
    return jsonify(data=x_data, hh_data=hh_datas, gp_data=gp_datas, zq_data=zq_datas, zs_data=zs_datas,
                   qdii_data=qdii_datas, fof_data=fof_datas)


def get_x_y_datas():
    # x_data = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    # x_data = ["2022/8/{}".format(i + 1) for i in range(21, 31)]
    date_instances = FundRand.query.filter_by(type='gp').order_by('date').all()
    dates = [i.date for i in date_instances]
    x_data = dates
    # 股票型
    gp_instances = FundRand.query.filter_by(type='gp').order_by('date').all()
    gp_datas = [i.last3month for i in gp_instances]
    # 债券型
    zq_instances = FundRand.query.filter_by(type='zq').order_by('date').all()
    zq_datas = [i.last3month for i in zq_instances]
    # 指数型
    zs_instances = FundRand.query.filter_by(type='zs').order_by('date').all()
    zs_datas = [i.last3month for i in zs_instances]
    # qdii型
    qdii_instances = FundRand.query.filter_by(type='qdii').order_by('date').all()
    qdii_datas = [i.last3month for i in qdii_instances]
    # fof型
    fof_instances = FundRand.query.filter_by(type='fof').order_by('date').all()
    fof_datas = [i.last3month for i in fof_instances]
    # 混合型
    hh_instances = FundRand.query.filter_by(type='hh').order_by('date').all()
    hh_datas = [i.last3month for i in hh_instances]
    # print('hh_datas', hh_datas)
    return x_data, gp_datas, zq_datas, zs_datas, qdii_datas, fof_datas, hh_datas


@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    # db.drop_all()
    db.create_all()
    app.run(debug=True, threaded=True)
    '''提供的方法
    /new 增加数据
    /show 显示所有数据
    /test 图表展示0
    /line1 图表展示1
    /line2 图表展示2
    '''
