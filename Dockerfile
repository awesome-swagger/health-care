FROM python:3.5

ENV CPATH=/usr/local/include/python3.5m

RUN mkdir /care_adopt_backend
WORKDIR /care_adopt_backend

ADD requirements.txt /care_adopt_backend/requirements.txt

ADD . /care_adopt_backend
ADD server /server