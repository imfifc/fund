FROM python:3.6
WORKDIR /Project/demo
RUN apt-get update && apt-get install -y curl vim  net-tools inetutils-ping dnsutils

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]