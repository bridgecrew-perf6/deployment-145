FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Shanghai

WORKDIR /app

COPY . /app

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y procps net-tools apt-utils \
    && ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone \
    && pip install pipenv -i https://mirrors.aliyun.com/pypi/simple/

RUN pipenv sync  && pipenv install --dev

RUN chmod +x /app/start.sh

ENTRYPOINT ["sh", "start.sh"]

