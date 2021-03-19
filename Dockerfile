FROM python:3.6-buster
ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code

RUN apt-get update && apt-get install libpq-dev -y tzdata && \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    python -m pip --no-cache install -U pip && \
    python -m pip --no-cache --use-feature=2020-resolver install -r requirements/production.txt
    
EXPOSE 8000
