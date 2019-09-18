FROM python:3.7
COPY ./bin/* /usr/bin/
COPY . /app
WORKDIR /app
RUN apt-get -y update; apt-get -y upgrade
RUN apt-get -y install vim uuid-runtime openslide-tools python3-openslide python3-opencv
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
