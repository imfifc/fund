### 环境信息
    python3.6   flask

##### 使用命令python start.py运行这个应用，打开浏览器，输入网址127.0.0.1:5000并回车，将会打开我们的网站。
安装依赖
```shell
yum install -y  python3-devel
```

###  Gunicorn + Gevent
 运行以下命令即可安装这两个利器
```shell
pip3 install gunicorn gevent
```
在根目录下新建文件 /gunicorn.conf.py
```
workers = 5    # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "gevent"   # 采用gevent库，支持异步处理请求，提高吞吐量
bind = "0.0.0.0:80"

```
编写start.py
可以使用gunicorn命令来测试是否可以正确运行，命令如下，打开网址127.0.0.1:80，将会打开我们的网站。
```shell
gunicorn start:app -c gunicorn.conf.py
```
一旦报错，则根据错误提示修复即可。

### 使用 Docker 封装 Flask 应用
```dockerfile
FROM python:3.6
WORKDIR /Project/demo

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]
```
构建镜像，运行容器
```shell
docker build  -t testfund:v1 .

docker run -d --network=host --name=fund testfund:v1

docker exec -it fund bash
```

### 创建定时任务 触发爬虫
```shell
0 1 * * *  docker exec stock2 /bin/sh -c 'wget localhost:8090/new > /dev/null 2>&1 &'

0 1 * * *  curl localhost:8090/new > /tmp/fund.txt 2>&1 &
```
### 使用 Docker-compose 封装 Flask 应用
```yaml
version: "3.7"
services:
  web:
    build: .
    container_name: fund
    volumes:
      - /etc/localtime:/etc/localtime
      - /root/.ssh:/root/.ssh
      - /tmp/fund.sqlite3:/Project/demo/fund/fund.sqlite3
    ports:
      - "8090:8090"
    privileged: true

    deploy:
      restart_policy:
        condition: on-failure
```


