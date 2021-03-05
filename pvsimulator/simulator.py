import random
import json
import logging
import pika
from csv_writer import write_row

logging.basicConfig(level=logging.INFO)

def pv_power_output(timestamp):
    return random.uniform(0, 3000)


def callback(ch, method, properties, body):
    logging.info(f"Received from meter: {body}")
    meter_msg = json.loads(body)

    pv_value = pv_power_output(meter_msg['timestamp'])
    total = pv_value + meter_msg['value']

    write_row({'timestamp': meter_msg['timestamp'],
               'meter_value': meter_msg['value'],
               'pv_value': pv_value,
               'sum': total})


def run_simulator():
    """Setup a RabbitMQ consumer on queue `meter`.

    For every recived message, lookup the corresponding PV value
    and write it to the `logs/output.csv` file"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='meter')

    channel.basic_consume(queue='meter', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    run_simulator()
