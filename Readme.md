# PV Simulator
This is some dummy program for a "homework" assignment for a job application.
The "problem" description can be found [here](docs/PV Simulator Challenge.pdf).

It basically consisted of two parts.
1. A power meter that simulates power consumption, sending it's data to a RabbitMQ broker.
2. A photovoltaic simulator, mocking a photovoltaic system producing power and adds the values read from the broker.

Why would anyone add values from a power producer to a power consumer instead of subtracting them?
I don't know, I don't care.

## Approach
Google for RabbitMQ as I've never used it, use `Pika` for python, [they say](https://www.rabbitmq.com/tutorials/tutorial-one-python.html).

Run the RabbitMQ producer and consumer in two different Docker containers, to simulate a bit of realism.

Write output to `out/logs.csv`.
Plot it, take a look.

# How to run
Tested with Python 3.9.2
## Command line
Set it up like this, I guess, I'm not running a Debian,
so it's not tested and therefore unlikely to work
(rather certainly, if you don't change the RMQ host).
Please just run it in docker (see below).
```bash
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq.service
python -m venv .venv  # optionally setup virtual env
pip install -r requirements.txt
```

Run
```bash
python pvsimulator/meter.py --realtime
```
for one message per second, or to just send the messages of a whole whole day at once
```bash
python pvsimulator/meter.py
```
Open another shell and exeute
```bash
python pvsimulator/simulator.py
```

## Docker
Docker-compose is a requirement here, I hope that's acceptable...
```bash
docker-compose build
docker-compose up
```



## Running the tests
No tests. Writing tests for a test is no fun.
I've got some actual code not properly testet around, sux.
