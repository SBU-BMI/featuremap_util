FROM python:3.7
COPY ./bin/* /usr/bin/
COPY . /app
WORKDIR /app/src
RUN apt-get -y update; apt-get -y upgrade
RUN apt-get -y install git vim uuid-runtime openslide-tools python3-openslide python3-opencv
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN echo 'Build done!'