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

docker build  --network=host -t testfund:v1 .
#docker run -itd --network=host --name=fund testfund:v1 bash
# 加root可以访问，同时setenforce 0
#docker run -d --network host --name fund  --privileged=true -v /tmp/fund/fund/fund.sqlite3:/Project/demo/fund/fund/fund.sqlite3 testfnd
docker run -d --network=host --name=fund testfund:v1

# 设置定时任务触发启动爬虫入库
0 1 * * *  docker exec stock2 /bin/sh -c 'wget localhost:8090/new > /dev/null 2>&1 &'
0 1 * * *  curl localhost:8090/new > /tmp/fund.txt 2>&1 &


#PS C:\Users\Administrator\Desktop\tengyun\fund\fund> $env:FLASK_APP = "server.py"
#flask run