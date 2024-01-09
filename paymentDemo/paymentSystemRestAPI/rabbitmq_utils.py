import pika
import time
from contextlib import contextmanager

def connect_to_rabbitmq():
    """Establishes a connection to RabbitMQ with retry logic."""
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

@contextmanager
def get_rabbitmq_channel():
    """Creates a RabbitMQ channel with proper connection handling."""
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    try:
        yield channel
    finally:
        channel.close()  # Close channel
        connection.close()  # Ensure connection closed