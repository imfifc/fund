from fund.server import app, db

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, threaded=True)
    '''提供的方法
    /new 增加数据
    /show 显示所有数据
    /test 图表展示0
    /line1 图表展示1
    /line2 图表展示2
    '''
