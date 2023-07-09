FROM python:3.10
WORKDIR /bots
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools \
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .