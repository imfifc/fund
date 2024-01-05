#!/usr/bin/env bash
#进行测试
gunicorn start:app -c gunicorn.conf.py
#while true ; do
##    sleep 43200   0.5day
#    wget localhost:8090/new
#    sleep 2
#
#done
# docker build  --network=host -t testfund:v1 .
docker build --no-cache  -t fund3 .

docker build  --network=host -t testfund:v1 .
#docker run -itd --network=host --name=fund testfund:v1 bash
# 加root可以访问，同时setenforce 0
#docker run -d --network host --name fund  --privileged=true -v /tmp/fund/fund/fund3.sqlite3:/Project/demo/fund/fund/fund3.sqlite3 testfnd
docker run -d --network=host --name=fund testfund:v1

# 设置定时任务触发启动爬虫入库
0 1 * * *  docker exec stock2 /bin/sh -c 'wget localhost:8090/new > /dev/null 2>&1 &'
0 1 * * *  curl localhost:8090/new > /tmp/fund.txt 2>&1 &


#PS C:\Users\Administrator\Desktop\tengyun\fund\fund> $env:FLASK_APP = "fund/server.py"
#flask run


#实际操作顺序:
#1.python app文件 db init  (或者flask db init)
#2.python 文件 db migrate -m "版本名(注释)"
#3.python 文件 db upgrade 然后观察表结构
#4.根据需求修改模型
#5.python 文件 db migrate -m "新版本名(注释)"
#6.python 文件 db upgrade 然后观察表结构
#7.若返回版本,则利用 python 文件 db history查看版本号
#8.python 文件 db downgrade(upgrade) 版本号

python manager.py db init
# 成功后, 在项目目录中会多出一个migration 的文件夹
# 迁移数据库, 这里可以做到数据表字段的增加删除等等
python manager.py db migrate
# 迁移后, 做更新操作
python manager.py db upgrade



model表数据调试
from fund.server import *
ctx = app.test_request_context()
ctx.push()
FundRand.query.filter_by(type='zs').order_by('date').all()
[<User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>, <User '汇添富中证光伏产业指数增强发起式A'>]
ctx.pop()
flask官方文档:https://dormousehole.readthedocs.io/en/latest/shell.html#id1