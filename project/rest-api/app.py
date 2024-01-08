import pika
import json
from flask import Flask, request, jsonify
from contextlib import contextmanager

app = Flask(__name__)


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
            time.sleep(2 ** attempt)  # Exponential backoff

    raise RuntimeError(f"Failed to connect to RabbitMQ after {max_retries} attempts")


@contextmanager
def get_rabbitmq_channel():
    """Creates a RabbitMQ channel with proper connection handling."""
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    try:
        yield channel
    finally:
        channel.close()  # Close the channel
        connection.close()  # Ensure connection closure


@app.route('/post', methods=['POST'])
def receive_message():
    """Receives a message and publishes it to the 'my_queue' queue."""
    data = request.json
    print(f'===== REST API Service =====', flush=True)
    print(f'data: {data}', flush=True)

    with get_rabbitmq_channel() as channel:
        channel.queue_declare(queue='my_queue')
        channel.basic_publish(exchange='', routing_key='my_queue', body=str(data))

    return 'Message published to queue', 201


@app.route('/payments', methods=['POST'])
def receive_payment():
    """Receives payment information and publishes it to the 'my_queue' queue."""
    data = request.json
    print('===== REST API Service =====', flush=True)
    print(f'data: {data}', flush=True)

    message = json.dumps(data)

    with get_rabbitmq_channel() as channel:    
        channel.queue_declare(queue='my_queue')
        channel.basic_publish(exchange='', routing_key='my_queue', body=message)

    return jsonify(message="Payment information published to queue"), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
