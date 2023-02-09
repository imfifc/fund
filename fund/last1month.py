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

# from fund.model import Last1month, db

# app = Flask(__name__, static_folder="static")  # static file 切记不要写错哦
import pymysql

# from fund import user
from fund import user, create_app
from fund.data import aggreate_data
from fund.models import Last1month, DayGrowRate, Last1month, Last6month, Last1week, Last1year
from fund.dbs import db
from fund.task import make_celery

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, r'fund/static/files')
UPLOAD_PATH = os.path.join(BASE_DIR, r'fund/static/files')
DOWNLOAD_FILES = os.listdir(UPLOAD_PATH)

app = create_app()


# celery = make_celery(app)
# pip
#
# @celery.task()
# def add_together(a, b):
#     return a + b


# result = add_together.delay(23, 42)
# result.wait()


def bar_base() -> Bar:
    # x_data = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    y_data = [820, 932, 901, 934, 1290, 1330, 1320]
    # 股票型
    x_data, gp_datas, zq_datas, zs_datas, qdii_datas, fof_datas, hh_datas = get_x_y_datas_2023()

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
        f = Last1month(**data)
        if not Last1month.query.filter_by(type=data.get('type'), date=data.get('date')).first():
            db.session.add(f)
        # db.session.add(f)
    db.session.commit()
    return jsonify(data=datas, code=200)


@app.route('/show')
def show():
    datas = Last1month.query.order_by(Last1month.date.desc()).all()
    # print(res)
    datas = [i.tojson() for i in datas]
    return render_template('show.html', datas=datas)


@app.route('/insert', methods=['POST', 'GET'])
def insert():
    # user = Last1month.query.filter_by(id=id).first()
    if request.method == "POST":
        # print('form', request.form.to_dict())
        form = request.form.to_dict()
        data = {
            'code': form.get('code'),
            'type': form.get('type'),
            'name': form.get('name'),
            'last1month': form.get('last1month'),
            'date': form.get('date'),
        }
        f = Last1month(**data)
        db.session.add(f)
        db.session.commit()
        return redirect(url_for('show'))

    return render_template('insert_fund.html')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    user = Last1month.query.filter_by(id=id).first()

    if request.method == "POST":
        # print('form', request.form.to_dict())
        form = request.form.to_dict()
        Last1month.query.filter_by(id=id).update(
            {'last1month': form.get('price'), 'date': form.get('date'), 'type': form.get('type')})
        db.session.commit()
        return redirect(url_for('show'))

    return render_template('update.html', user=user)


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    user = Last1month.query.filter_by(id=id).first()

    if request.method == "POST":
        # print('form', request.form.to_dict())
        # form = request.form.to_dict()
        Last1month.query.filter_by(id=id).delete()
        db.session.commit()
        # return '删除成功'
        return redirect(url_for('show'))

    return render_template('delete_fund.html', user=user)


@app.route('/batch_delete/<date>', methods=['POST', 'GET'])
def batch_delete(date):
    user = Last1month.query.filter_by(date=date).first()

    if request.method == "POST":
        # print('form', request.form.to_dict())
        # form = request.form.to_dict()
        Last1month.query.filter_by(date=date).delete()
        db.session.commit()
        # return '删除成功'
        return redirect(url_for('show'))

    return render_template('batch_delete.html', user=user)


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
    x_data, gp_datas, zq_datas, zs_datas, qdii_datas, fof_datas, hh_datas = get_x_y_datas_2023()
    return jsonify(data=x_data, hh_data=hh_datas, gp_data=gp_datas, zq_data=zq_datas, zs_data=zs_datas,
                   qdii_data=qdii_datas, fof_data=fof_datas)


def filter_condition(kind, start_time, end_time: str):
    return Last1month.query.filter_by(type=kind).filter(Last1month.date >= start_time,
                                                        Last1month.date <= end_time).order_by('date').all()


def get_x_y_datas_2022():
    # x_data = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    # x_data = ["2022/8/{}".format(i + 1) for i in range(21, 31)]
    # date_instances = Last1month.query.filter_by(type='gp').order_by('date').all()
    date_instances = filter_condition('gp', '2022-01-01', '2022-12-12')
    dates = [i.date for i in date_instances]
    x_data = dates
    # 股票型
    gp_instances = filter_condition('gp', '2022-01-01', '2022-12-12')
    gp_datas = [i.last1month for i in gp_instances]
    # 债券型
    zq_instances = filter_condition('zq', '2022-01-01', '2022-12-12')
    zq_datas = [i.last1month for i in zq_instances]
    # 指数型
    zs_instances = filter_condition('zs', '2022-01-01', '2022-12-12')
    zs_datas = [i.last1month for i in zs_instances]
    # qdii型
    qdii_instances = filter_condition('qdii', '2022-01-01', '2022-12-12')
    qdii_datas = [i.last1month for i in qdii_instances]
    # fof型
    fof_instances = filter_condition('fof', '2022-01-01', '2022-12-12')
    fof_datas = [i.last1month for i in fof_instances]
    # 混合型
    hh_instances = filter_condition('hh', '2022-01-01', '2022-12-12')
    hh_datas = [i.last1month for i in hh_instances]
    # print('hh_datas', hh_datas)
    return x_data, gp_datas, zq_datas, zs_datas, qdii_datas, fof_datas, hh_datas


def get_x_y_datas_2023():
    # x_data = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    # x_data = ["2022/8/{}".format(i + 1) for i in range(21, 31)]
    # date_instances = Last1month.query.filter_by(type='gp').order_by('date').all()
    date_instances = filter_condition('gp', '2023-01-01', '2023-12-12')
    dates = [i.date for i in date_instances]
    x_data = dates
    # 股票型
    gp_instances = filter_condition('gp', '2023-01-01', '2023-12-12')
    gp_datas = [i.last1month for i in gp_instances]
    # 债券型
    zq_instances = filter_condition('zq', '2023-01-01', '2023-12-12')
    zq_datas = [i.last1month for i in zq_instances]
    # 指数型
    zs_instances = filter_condition('zs', '2023-01-01', '2023-12-12')
    zs_datas = [i.last1month for i in zs_instances]
    # qdii型
    qdii_instances = filter_condition('qdii', '2023-01-01', '2023-12-12')
    qdii_datas = [i.last1month for i in qdii_instances]
    # fof型
    fof_instances = filter_condition('fof', '2023-01-01', '2023-12-12')
    fof_datas = [i.last1month for i in fof_instances]
    # 混合型
    hh_instances = filter_condition('hh', '2023-01-01', '2023-12-12')
    hh_datas = [i.last1month for i in hh_instances]
    # print('hh_datas', hh_datas)
    return x_data, gp_datas, zq_datas, zs_datas, qdii_datas, fof_datas, hh_datas


def get_x_y_datas():
    # x_data = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    # x_data = ["2022/8/{}".format(i + 1) for i in range(21, 31)]
    date_instances = Last1month.query.filter_by(type='gp').order_by('date').all()
    dates = [i.date for i in date_instances]
    x_data = dates
    # 股票型
    gp_instances = Last1month.query.filter_by(type='gp').order_by('date').all()
    gp_datas = [i.last1month for i in gp_instances]
    # 债券型
    zq_instances = Last1month.query.filter_by(type='zq').order_by('date').all()
    zq_datas = [i.last1month for i in zq_instances]
    # 指数型
    zs_instances = Last1month.query.filter_by(type='zs').order_by('date').all()
    zs_datas = [i.last1month for i in zs_instances]
    # qdii型
    qdii_instances = Last1month.query.filter_by(type='qdii').order_by('date').all()
    qdii_datas = [i.last1month for i in qdii_instances]
    # fof型
    fof_instances = Last1month.query.filter_by(type='fof').order_by('date').all()
    fof_datas = [i.last1month for i in fof_instances]
    # 混合型
    hh_instances = Last1month.query.filter_by(type='hh').order_by('date').all()
    hh_datas = [i.last1month for i in hh_instances]
    # print('hh_datas', hh_datas)
    return x_data, gp_datas, zq_datas, zs_datas, qdii_datas, fof_datas, hh_datas


@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        # 使用request.FILES['myfile']获得文件流对象file
        file = request.files['myfile']
        # 文件储存路径，应用settings中的配置，file.name获取文件名
        new_file = os.path.join(MEDIA_ROOT, secure_filename(file.filename))
        print(file.filename)
        print(secure_filename(file.filename))
        print(new_file)
        if not os.path.exists(new_file):
            # file.save(new_file)
            file.save(new_file)
            return 'file uploaded successfully'
        else:
            return 'file exist, please change file'


@app.route('/download', methods=['GET'])
def download():
    if request.method == "GET":
        print(UPLOAD_PATH)
        files = os.listdir(UPLOAD_PATH)
        return render_template('download.html', files=files)


@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.isfile(os.path.join(UPLOAD_PATH, filename))
    if path:
        response = make_response(
            send_from_directory(UPLOAD_PATH, filename.encode('utf-8').decode('utf-8'), as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
        return response


if __name__ == "__main__":
    # db.drop_all()
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run(debug=True, threaded=True, port=8080)

    '''提供的方法
    /new 增加数据
    /show 显示所有数据
    /test 图表展示0
    /line1 图表展示1
    /line2 图表展示2
    /insert 插入数据
     update delete 
     todo: login cookie session model拆分，蓝图
     
     /user [
        /
        /profile
     ]
    '''
