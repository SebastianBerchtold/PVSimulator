import json
import logging
import pika
from datetime import datetime, timezone
from pysolar.solar import get_altitude, radiation
from csv_writer import write_row

logging.basicConfig(level=logging.INFO)


def solar_radiation(timestamp: datetime):
    """Returns radiaton in W/m^2 for Munich at time `timestamp`.

    This simulation comes directly from my heart,
    it's always sunny, no dark clouds around here.
    """
    # St.-Cajetan-Straße 43 Munich
    lat, lon = 48.12046607369282, 11.60234104352835

    # yeah yeah, one or two hours off, I don't care
    timestamp = datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc)

    try:  # for some reason this is failing, every once in a while
        altitude_deg = get_altitude(lat, lon, timestamp)
        rad = radiation.get_radiation_direct(timestamp, altitude_deg)
    except OverflowError:
        logging.info(f"Solar radiation calc failing for time {timestamp}")
        rad = 0.0

    return rad


def pv_power_output(timestamp: datetime):
    """Returns PV power in $\frac{W}{m^2}$ for Munich at time `timestamp`."""
    pv_size = 20  # m^2
    eta = 0.22 + 0.1  # best solar panel conversion efficencey ever
    return eta * solar_radiation(timestamp) * pv_size


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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='meter')

    channel.basic_consume(queue='meter', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    run_simulator()
