import time
import datetime
import json
import random
import pika


def next_meter_value(value):
    """Parameters
    ----------
    value : float
        Current power consumtion in Watt, haha.

    Returns
    -------
    float
        Next measured value
    """
    # Turn one of infinetly many LEDs on or off.
    # Allmost all of them are burned, so they
    # consume power according to the spec.
    value += random.uniform(-3.0, 3.0)

    # We wanna make sure our fuse doesn't burn.
    # Also there's no light shining on them,
    # and we're not building a perpetuum mobile,
    # because this is obviously a realistic simulation ...
    value = max(0, min(9000, value))
    return value


def send_meter_value(channel, timestamp, value):
    """Publish meter value in json format"""
    body = {'timestamp': timestamp.isoformat(),
            'value': value}
    channel.basic_publish(exchange='', routing_key='meter',
                          body=json.dumps(body))


def simulate_power_meter(channel):
    meter_value = 0  # power consumtion
    while True:
        meter_value = next_meter_value(meter_value)
        send_meter_value(channel, datetime.datetime.now(), meter_value)
        time.sleep(1.0)


def run_meter():
    """Setup RabbitMQ channel `meter` and publish some random shit."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='meter')

    simulate_power_meter(channel)
    connection.close()


if __name__ == '__main__':
    run_meter()
