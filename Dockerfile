FROM python:3

WORKDIR /usr/src/app

RUN git clone https://ruslanbeyganov@bitbucket.org/courstore/telethon-module.git

RUN pip3 install --upgrade telethon
RUN pip3 install quart
RUN pip3 install quart_schema
RUN apt-get update && apt-get -y install python3-quart

CMD [ "bootstrap.sh" ]