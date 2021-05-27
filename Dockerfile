FROM ubuntu:21.04

WORKDIR /Automaton

COPY requirements.txt requirements.txt

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install libglib2.0-0 libgirepository-1.0-1

# ENV TZ=Asia/Dubai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt install -y tzdata

RUN apt-get -y install python3-pip

RUN pip3 install -r requirements.txt

COPY Automaton .

CMD [ "sudo", "python3.9", "./lib.py"]
