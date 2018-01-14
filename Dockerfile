FROM python:3.6.3

MAINTAINER Heri Rusmanto "hvedaid@gmail.com"

# Set working directory
RUN mkdir -p /code
WORKDIR /code

# Add requirements (to leverage Docker cache)
ADD ./requirements.txt /code/requirements.txt
# install requirements
RUN pip install -r requirements.txt

ADD . /code
