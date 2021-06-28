FROM ubuntu:21.04

WORKDIR /automaton

COPY requirements.txt requirements.txt

# Setup tzdata
# Change to your time zone.
ENV TZ=Asia/Dubai 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt install -y tzdata

RUN apt-get -y install python3-pip

RUN pip3 install -r requirements.txt

COPY automaton .

CMD [ "sudo", "python3.9", "automaton/__init__.py"]
