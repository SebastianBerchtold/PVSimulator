FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

RUN chmod +x wait-for-it.sh
ENTRYPOINT [ "./wait-for-it.sh", "rabbitmq:5672", "--" ]
