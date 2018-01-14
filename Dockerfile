FROM python:3.6.3

MAINTAINER Heri Rusmanto "hvedaid@gmail.com"

RUN mkdir -p /var/www/kalikesia
WORKDIR /var/www/kalikesia

ADD requirements.txt /var/www/kalikesia
RUN pip install -r requirements.txt

ADD . /var/www/kalikesia