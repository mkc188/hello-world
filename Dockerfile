FROM python:2.7
RUN apt-get -y update
RUN apt-get -y install python python-dev python-pip libev-dev gcc
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
