FROM python:3.10-alpine3.18
WORKDIR /bots
RUN pip install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip install aiogram==3.0.0b7
RUN chmod 755 .
COPY . .