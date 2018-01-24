FROM python:3.6.3

MAINTAINER Heri Rusmanto "hvedaid@gmail.com"

# Set working directory
RUN mkdir -p /var/www/kalikesia
WORKDIR /var/www/kalikesia

# Add requirements (to leverage Docker cache)
ADD requirements.txt /var/www/kalikesia

# Install requirements
RUN pip install -r requirements.txt

ADD . /var/www/kalikesia
