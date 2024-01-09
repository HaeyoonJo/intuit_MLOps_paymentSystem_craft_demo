import pika
import time
from contextlib import contextmanager

def create_connection():
    max_retries = 5
    parameters = pika.ConnectionParameters(
        'rabbitmq', credentials=pika.PlainCredentials('admin', 'admin'), heartbeat=10
    )

    for attempt in range(max_retries):
        try:
            return pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(2 ** attempt)

    raise RuntimeError(f"Failed to connect to RabbitMQ after {max_retries} attempts")

def setup_channel(connection):
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')
    return channel