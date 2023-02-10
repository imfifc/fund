from flask import render_template

from fund import create_app
from fund.models import FundRand, DayGrowRate, Last1month, Last6month, Last1week, Last1year
from fund.dbs import db
app = create_app()


@app.route('/show')
def show():
    datas = FundRand.query.order_by(FundRand.date.desc()).all()
    # print(res)
    datas = [i.tojson() for i in datas]
    return render_template('show.html', datas=datas)


@app.route('/showDayGrowRate')
def show_day_grow_rate():
    datas = DayGrowRate.query.order_by(DayGrowRate.date.desc()).all()
    # print(res)
    datas = [i.tojson() for i in datas]
    print(datas)
    return render_template('showDayGrowRate.html', datas=datas)
